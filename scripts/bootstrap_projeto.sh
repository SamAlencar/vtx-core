#!/usr/bin/env bash
# Cria um repositório de cliente a partir de templates/projeto/.
# Uso: scripts/bootstrap_projeto.sh <nome> <destino>
set -euo pipefail

uso() {
  echo "Uso: $0 <nome> <destino>" >&2
  echo "Exemplo: $0 demo /tmp/demo" >&2
  exit 2
}

[[ $# -eq 2 ]] || uso
NOME="$1"
DEST="$2"

if [[ ! "$NOME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "Nome inválido: $NOME (use letras, números, ponto, _ ou -)" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/templates/projeto"
if [[ ! -d "$SRC" ]]; then
  echo "Template não encontrado: $SRC" >&2
  exit 1
fi

if [[ -e "$DEST" ]]; then
  if [[ ! -d "$DEST" ]]; then
    echo "Destino existe e não é diretório: $DEST" >&2
    exit 1
  fi
  if [[ -n "$(ls -A "$DEST" 2>/dev/null)" ]]; then
    echo "Destino não está vazio: $DEST" >&2
    exit 1
  fi
else
  mkdir -p "$DEST"
fi

DEST="$(cd "$DEST" && pwd)"

# Copia incluindo arquivos ocultos, sem sobrepor o destino por engano.
shopt -s dotglob
cp -a "$SRC"/. "$DEST"/
shopt -u dotglob

# Regras de tokens/contexto vêm da fonte do vtx-core.
# As regras por papel ficam as do template (caminhos válidos no cliente).
mkdir -p "$DEST/.cursor/rules"
cp "$ROOT/.cursor/rules/eficiencia-de-tokens.mdc" "$DEST/.cursor/rules/"
cp "$ROOT/.cursor/rules/economia-de-contexto.mdc" "$DEST/.cursor/rules/"

# Troca o placeholder em arquivos de texto.
while IFS= read -r -d '' arquivo; do
  if grep -q '__NOME_DO_PROJETO__' "$arquivo" 2>/dev/null; then
    sed -i "s/__NOME_DO_PROJETO__/${NOME}/g" "$arquivo"
  fi
done < <(find "$DEST" -type f ! -path '*/.git/*' -print0)

if [[ ! -d "$DEST/.git" ]]; then
  git -C "$DEST" init -q
fi

echo "Projeto '$NOME' criado em $DEST"
