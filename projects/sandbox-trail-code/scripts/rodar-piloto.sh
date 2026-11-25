#!/usr/bin/env bash
# Piloto VTX-135: instala o graft do pin e roda só comandos locais, sem init e sem --deep.
set -euo pipefail

SANDBOX="$(cd "$(dirname "$0")/.." && pwd)"
VTX_CORE="$(cd "$SANDBOX/../.." && pwd)"
export DO_NOT_TRACK=1
export HOME="$SANDBOX/.home"
export npm_config_cache="$SANDBOX/.npm-cache"
mkdir -p "$HOME" "$npm_config_cache" "$SANDBOX/exemplos/saida-bruta"

cd "$SANDBOX"
if [[ ! -f "$SANDBOX/package-lock.json" ]]; then
  echo "package-lock.json ausente; não instalar sem a árvore travada" >&2
  exit 1
fi
if [[ ! -x "$SANDBOX/node_modules/.bin/graft" ]]; then
  echo "Instalando a árvore do package-lock com DO_NOT_TRACK=1 e --ignore-scripts (sem -g)..."
  npm ci --ignore-scripts --no-fund --no-audit
fi

GRAFT="$SANDBOX/node_modules/.bin/graft"
[[ -x "$GRAFT" ]] || { echo "graft não encontrado após o npm ci" >&2; exit 1; }

echo "=== versão ==="
"$GRAFT" --version || true

echo "=== telemetry disable + status ==="
"$GRAFT" telemetry disable || true
"$GRAFT" telemetry status || true

ALVO="$SANDBOX/tmp-repo"
rm -rf "$ALVO"
# Cópia rasa só com o necessário para um build local, sem o .git de worktree compartilhado.
mkdir -p "$ALVO"
git -C "$VTX_CORE" checkout-index -a --prefix="$ALVO/"
git -C "$ALVO" init -q
git -C "$ALVO" add -A
git -C "$ALVO" -c user.email="piloto@local" -c user.name="piloto" commit -qm "piloto"

echo "=== graft build (sem --deep) ==="
START=$(date +%s)
"$GRAFT" build "$ALVO" | tee "$SANDBOX/exemplos/saida-bruta/build.log"
END=$(date +%s)
echo "tempo_build_s=$((END-START))" | tee "$SANDBOX/exemplos/saida-bruta/tempo-build.txt"

ARQ_REL="scripts/backlog_lib.py"
echo "=== skeleton vs arquivo completo ($ARQ_REL) ==="
"$GRAFT" skeleton "$ARQ_REL" "$ALVO" > "$SANDBOX/exemplos/saida-bruta/skeleton-backlog_lib.txt"
python3 - << PY
from pathlib import Path
sandbox = Path("$SANDBOX")
alvo = Path("$ALVO")
full = (alvo / "$ARQ_REL").read_text(encoding="utf-8")
skel = (sandbox / "exemplos/saida-bruta/skeleton-backlog_lib.txt").read_text(encoding="utf-8")
# aproximação comum: 1 token ≈ 4 caracteres
def toks(s):
    return round(len(s) / 4)
linhas = [
    f"arquivo={'$ARQ_REL'}",
    f"completo_bytes={len(full.encode())}",
    f"completo_linhas={full.count(chr(10))+1}",
    f"completo_tokens_aprox={toks(full)}",
    f"skeleton_bytes={len(skel.encode())}",
    f"skeleton_linhas={skel.count(chr(10))+1}",
    f"skeleton_tokens_aprox={toks(skel)}",
    f"razao_tokens={toks(skel)/toks(full) if toks(full) else 'n/a'}",
]
(sandbox / "exemplos/saida-bruta/skeleton-medida.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
PY

echo "=== ask (sem LLM) ==="
"$GRAFT" ask "como o backlog escolhe a próxima tarefa" "$ALVO" \
  > "$SANDBOX/exemplos/saida-bruta/ask-proxima-tarefa.txt" || true
wc -c "$SANDBOX/exemplos/saida-bruta/ask-proxima-tarefa.txt"

echo "=== check (sem learnings, esperado não conflitante) ==="
"$GRAFT" check "$ALVO" > "$SANDBOX/exemplos/saida-bruta/check.txt" 2>&1 || true

echo "=== stats ==="
"$GRAFT" stats "$ALVO" > "$SANDBOX/exemplos/saida-bruta/stats.txt" 2>&1 || true
cat "$SANDBOX/exemplos/saida-bruta/stats.txt"

# Sanitiza uma amostra curta para versionar (sem despejar o grafo inteiro).
python3 - << PY
from pathlib import Path
p = Path("$SANDBOX/exemplos/saida-bruta/ask-proxima-tarefa.txt")
texto = p.read_text(encoding="utf-8", errors="replace")
Path("$SANDBOX/exemplos/saida-bruta/ask-proxima-tarefa-amostra.txt").write_text(texto[:2000] + ("\n… [recorte]\n" if len(texto) > 2000 else ""), encoding="utf-8")
PY

echo "Piloto concluído. HOME isolado em $HOME"
# Recusa se alguém tiver rodado init neste sandbox.
if [[ -d "$ALVO/.trail" ]] || [[ -d "$SANDBOX/.trail" ]]; then
  echo "AVISO: apareceu .trail/ — verificar se init rodou" >&2
fi
