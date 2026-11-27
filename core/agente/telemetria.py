"""Telemetria por execução de agente (VTX-179).

Uma linha JSON por execução (run_id, trace_id, cliente, tokens, custo, duração),
com redação de PII, soma de custo por cliente e dia e orçamento diário que
interrompe a execução antes de gastar. Só biblioteca padrão.
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

# Ordem importa: tokens antes de números longos.
_PADROES = [
    (re.compile(r"(?i)\bbearer\s+[a-z0-9._~+/=-]{8,}"), "Bearer [TOKEN]"),
    (re.compile(r"\b(?:sk|pk|rk)-[A-Za-z0-9_-]{16,}"), "[TOKEN]"),
    (re.compile(r"\b(?:ghp|gho|ghs|github_pat)_[A-Za-z0-9_]{20,}"), "[TOKEN]"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), "[TOKEN]"),
    (re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[EMAIL]"),
    (re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"), "[CPF]"),
]


def redigir(valor: Any) -> Any:
    """Troca CPF, e-mail e tokens por marcadores, em str, dict e list."""
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
    """O cliente já gastou o orçamento do dia: a execução não começa."""


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
    if not caminho.exists():
        return []
    return [json.loads(x) for x in caminho.read_text(encoding="utf-8").splitlines() if x.strip()]


def custo_por_cliente_dia(linhas: Iterable[dict]) -> dict[tuple[str, str], float]:
    """Soma custo_usd por (cliente, dia UTC AAAA-MM-DD)."""
    total: dict[tuple[str, str], float] = defaultdict(float)
    for x in linhas:
        total[(x["cliente"], x["ts"][:10])] += x["custo_usd"]
    return {k: round(v, 6) for k, v in total.items()}


class Telemetria:
    """Grava execuções em JSONL e aplica orçamento diário por cliente (US$)."""

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
        linha = redigir(asdict(ex))
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
        return linha

    @contextmanager
    def execucao(self, cliente: str, agente: str, modelo: str = "",
                 trace_id: str = "") -> Iterator[Execucao]:
        """Checa o orçamento, mede a duração e grava uma linha mesmo se falhar."""
        self.checar_orcamento(cliente)
        ex = Execucao(cliente=cliente, agente=agente, modelo=modelo,
                      trace_id=trace_id or uuid.uuid4().hex)
        inicio = time.monotonic()
        try:
            yield ex
        except Exception as e:
            ex.status, ex.erro = "erro", f"{type(e).__name__}: {e}"
            raise
        finally:
            ex.duracao_ms = int((time.monotonic() - inicio) * 1000)
            self.registrar(ex)
