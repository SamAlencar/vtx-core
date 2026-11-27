#!/usr/bin/env bash
# Guarda de DADOS para os testes ao vivo de Postgres do template web.
# Source neste arquivo (não execute). O chamador pode definir NOME para as
# mensagens. Só aceita, depois de realpath -m (resolve '..' e symlinks):
#   /workspace/pg-acoes-<algo>     (filho direto de /workspace)
#   ${TMPDIR:-/tmp}/pg-acoes-<algo>  (padrão do mktemp dos scripts)
# Recusa vazio, /, /workspace, qualquer outra pasta, travessia, symlink que
# aponte para fora desses padrões, e o data dir da Evolution.

validar_dados() {
  local bruto="${1-}"
  local prefixo="${NOME:-guarda_dados_pg}"
  if [[ -z "$bruto" || "$bruto" == "/" ]]; then
    echo "$prefixo: recuso DADOS vazio ou /." >&2
    exit 2
  fi
  local canon
  canon="$(realpath -m -- "$bruto")" || {
    echo "$prefixo: não consegui normalizar DADOS." >&2
    exit 2
  }
  if [[ -z "$canon" || "$canon" == "/" ]]; then
    echo "$prefixo: recuso DADOS vazio ou /." >&2
    exit 2
  fi
  if [[ "$canon" == *evolution-pgdata* ]]; then
    echo "$prefixo: recuso usar o data dir da Evolution." >&2
    exit 2
  fi

  local pai base tmp
  pai="$(dirname -- "$canon")"
  base="$(basename -- "$canon")"
  tmp="$(realpath -m -- "${TMPDIR:-/tmp}")"

  if [[ "$base" != pg-acoes-* || "$base" == "pg-acoes-" ]]; then
    echo "$prefixo: recuso DADOS (o diretório deve se chamar pg-acoes-*): $canon" >&2
    exit 2
  fi
  if [[ "$pai" == "/workspace" || "$pai" == "$tmp" ]]; then
    DADOS="$canon"
    return 0
  fi
  echo "$prefixo: recuso DADOS fora de /workspace/pg-acoes-* ou ${tmp}/pg-acoes-*: $canon" >&2
  exit 2
}

remover_dados() {
  validar_dados "$DADOS"
  rm -rf -- "$DADOS"
}
