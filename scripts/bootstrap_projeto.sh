#!/usr/bin/env bash
# Cria um repositório de cliente a partir do template.
# Uso: scripts/bootstrap_projeto.sh [--tipo python|web] <nome> <destino>
set -euo pipefail

uso() {
  echo "Uso: $0 [--tipo python|web] <nome> <destino>" >&2
  echo "Exemplo: $0 demo /tmp/demo" >&2
  echo "         $0 --tipo web demo /tmp/demo" >&2
  echo "O padrão é --tipo python (templates/projeto/)." >&2
  exit 2
}

TIPO="python"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tipo)
      [[ $# -ge 2 ]] || uso
      TIPO="$2"
      shift 2
      ;;
    --tipo=*)
      TIPO="${1#--tipo=}"
      shift
      ;;
    -h|--help)
      uso
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Opção desconhecida: $1" >&2
      uso
      ;;
    *)
      break
      ;;
  esac
done

[[ $# -eq 2 ]] || uso
NOME="$1"
DEST="$2"

case "$TIPO" in
  python) SRC_REL="templates/projeto" ;;
  web) SRC_REL="templates/web-next" ;;
  *)
    echo "Tipo inválido: $TIPO (use python ou web)" >&2
    exit 2
    ;;
esac

if [[ ! "$NOME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "Nome inválido: $NOME (use letras, números, ponto, _ ou -)" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/$SRC_REL"
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
# Não leva node_modules/ nem .next/ se alguém gerou o template localmente.
shopt -s dotglob
cp -a "$SRC"/. "$DEST"/
shopt -u dotglob
rm -rf "$DEST/node_modules" "$DEST/.next" "$DEST/out" "$DEST/coverage"

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
done < <(find "$DEST" -type f ! -path '*/.git/*' ! -path '*/node_modules/*' -print0)

if [[ ! -d "$DEST/.git" ]]; then
  git -C "$DEST" init -q
fi

echo "Projeto '$NOME' ($TIPO) criado em $DEST"
