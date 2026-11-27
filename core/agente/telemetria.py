"""Telemetria por execução de agente (VTX-179).

Uma linha JSON por execução (run_id, trace_id, cliente, tokens, custo, duração),
com redação de PII, soma de custo por cliente e dia e orçamento diário aplicado
como limite brando (checado na entrada da execução). Só biblioteca padrão.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from collections import defaultdict
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Identificadores da linha: não passam por redigir(), senão e-mail como
# cliente vira [EMAIL] e o orçamento deixa de achar o gasto.
_CAMPOS_IDENTIDADE = frozenset({"cliente", "agente", "run_id", "trace_id"})

# Ordem importa: tokens antes de números. CPF/telefone sem máscara (11 dígitos)
# ficam de fora de propósito, para não tratar celular como CPF.
_PADROES = [
    (re.compile(r"(?i)\bbearer\s+[a-z0-9._~+/=-]{8,}"), "Bearer [TOKEN]"),
    (re.compile(r"\b(?:sk|pk|rk)-[A-Za-z0-9_-]{16,}"), "[TOKEN]"),
    (re.compile(r"\b(?:ghp|gho|ghs|github_pat)_[A-Za-z0-9_]{20,}"), "[TOKEN]"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), "[TOKEN]"),
    (re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[EMAIL]"),
    (re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"), "[CNPJ]"),
    (re.compile(r"\b\d{14}\b"), "[CNPJ]"),
    (re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"), "[CPF]"),
    (re.compile(r"\(\d{2}\)\s*\d{4,5}-\d{4}"), "[TELEFONE]"),
    (re.compile(r"\b\d{2}\s\d{4,5}-\d{4}\b"), "[TELEFONE]"),
]


def redigir(valor: Any) -> Any:
    """Troca CPF/CNPJ com máscara, telefone com máscara, e-mail e tokens por marcadores."""
    if isinstance(valor, str):
        for padrao, troca in _PADROES:
            valor = padrao.sub(troca, valor)
        return valor
    if isinstance(valor, dict):
        return {k: redigir(v) for k, v in valor.items()}
    if isinstance(valor, list | tuple):
        return [redigir(v) for v in valor]
    return valor


def custo_usd(tokens_entrada: int, tokens_saida: int, preco_entrada_mtok: float,
              preco_saida_mtok: float) -> float:
    """Custo em US$ a partir do preço por milhão de tokens."""
    return round((tokens_entrada * preco_entrada_mtok + tokens_saida * preco_saida_mtok) / 1e6, 6)


class OrcamentoExcedido(RuntimeError):
    """O cliente já atingiu o orçamento do dia na última conferência de entrada."""


@dataclass
class Execucao:
    cliente: str
    agente: str
    modelo: str = ""
    trace_id: str = ""
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    tokens_entrada: int = 0
    tokens_saida: int = 0
    custo_usd: float = 0.0
    duracao_ms: int = 0
    status: str = "ok"
    erro: str | None = None
    ts: str = ""

    def somar(self, tokens_entrada: int, tokens_saida: int, custo: float) -> None:
        self.tokens_entrada += tokens_entrada
        self.tokens_saida += tokens_saida
        self.custo_usd = round(self.custo_usd + custo, 6)


def ler(caminho: Path) -> list[dict]:
    """Linhas JSON válidas. Linhas corrompidas são ignoradas (ver ler_detalhado)."""
    linhas, _ = ler_detalhado(caminho)
    return linhas


def ler_detalhado(caminho: Path) -> tuple[list[dict], int]:
    """Devolve (linhas válidas, quantidade de linhas com JSON inválido)."""
    if not caminho.exists():
        return [], 0
    ok: list[dict] = []
    invalidas = 0
    for x in caminho.read_text(encoding="utf-8").splitlines():
        if not x.strip():
            continue
        try:
            item = json.loads(x)
        except json.JSONDecodeError:
            invalidas += 1
            continue
        if isinstance(item, dict):
            ok.append(item)
        else:
            invalidas += 1
    return ok, invalidas


def custo_por_cliente_dia(linhas: Iterable[dict]) -> dict[tuple[str, str], float]:
    """Soma custo_usd por (cliente, dia UTC AAAA-MM-DD)."""
    total: dict[tuple[str, str], float] = defaultdict(float)
    for x in linhas:
        try:
            total[(x["cliente"], x["ts"][:10])] += x["custo_usd"]
        except (KeyError, TypeError):
            continue
    return {k: round(v, 6) for k, v in total.items()}


class Telemetria:
    """Grava execuções em JSONL e aplica orçamento diário por cliente (US$).

    O orçamento é um limite brando: só é conferido na entrada de `execucao()`.
    Uma execução já iniciada pode passar do limite, e execuções paralelas podem
    ler o mesmo gasto e passar juntas. `gasto_hoje` relê o arquivo inteiro a
    cada conferência; em produção isso pede rotação diária ou um agregado.
    """

    def __init__(self, caminho: Path, orcamento_dia: dict[str, float] | None = None,
                 orcamento_padrao: float | None = None,
                 agora: Callable[[], datetime] = lambda: datetime.now(UTC)) -> None:
        self.caminho = Path(caminho)
        self.orcamento_dia = orcamento_dia or {}
        self.orcamento_padrao = orcamento_padrao
        self.agora = agora

    def gasto_hoje(self, cliente: str) -> float:
        hoje = self.agora().strftime("%Y-%m-%d")
        return custo_por_cliente_dia(ler(self.caminho)).get((cliente, hoje), 0.0)

    def checar_orcamento(self, cliente: str) -> None:
        limite = self.orcamento_dia.get(cliente, self.orcamento_padrao)
        if limite is not None and self.gasto_hoje(cliente) >= limite:
            raise OrcamentoExcedido(f"orçamento diário de {cliente} esgotado (US$ {limite})")

    def registrar(self, ex: Execucao) -> dict:
        ex.ts = ex.ts or self.agora().isoformat()
        bruto = asdict(ex)
        linha = {k: (v if k in _CAMPOS_IDENTIDADE else redigir(v)) for k, v in bruto.items()}
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
        return linha

    @contextmanager
    def execucao(self, cliente: str, agente: str, modelo: str = "",
                 trace_id: str = "") -> Iterator[Execucao]:
        """Checa o orçamento na entrada, mede a duração e grava uma linha mesmo se falhar."""
        self.checar_orcamento(cliente)
        ex = Execucao(cliente=cliente, agente=agente, modelo=modelo,
                      trace_id=trace_id or uuid.uuid4().hex)
        inicio = time.monotonic()
        try:
            yield ex
        except BaseException as e:
            ex.status, ex.erro = "erro", f"{type(e).__name__}: {e}"
            raise
        finally:
            ex.duracao_ms = int((time.monotonic() - inicio) * 1000)
            self.registrar(ex)
