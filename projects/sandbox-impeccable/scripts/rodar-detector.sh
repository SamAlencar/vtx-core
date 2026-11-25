#!/bin/bash
# Baixa o engine 0.1.27 (linux-x64), confere SHA-256 e roda detect na tela de teste.
# Não instala hooks. Telemetria desligada. Sem login.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export DO_NOT_TRACK=1
export IMPECCABLE_NO_TELEMETRY=1
export IMPECCABLE_HOME="$ROOT/.impeccable-home"
VER="0.1.27"
ASSET="impeccable-linux-x64"
SHA="41d66e945bcdfc560005b61ad0b6b2312b124890039262f2e63322ef2709ccfd"
URL="https://github.com/pbakaus/impeccable/releases/download/engine-v${VER}/${ASSET}"
BIN_DIR="$ROOT/bin/linux-x64"
BIN="$BIN_DIR/impeccable"
mkdir -p "$BIN_DIR"
if [[ ! -x "$BIN" ]]; then
  echo "baixando $URL"
  curl -fsSL -o "$BIN" "$URL"
  chmod +x "$BIN"
fi
got=$(sha256sum "$BIN" | awk '{print $1}')
if [[ "$got" != "$SHA" ]]; then
  echo "SHA-256 não bate: esperado $SHA, obtido $got" >&2
  rm -f "$BIN"
  exit 1
fi
echo "checksum ok ($SHA)"
ls -lh "$BIN"
echo "--- telemetry status ---"
"$BIN" telemetry status || true
echo "--- detect ---"
TIMEFORMAT='tempo_real=%R s'
set +e
{ time "$BIN" detect --json "$ROOT/tela-teste/index.html" > "$ROOT/detect-saida.json"; } 2> "$ROOT/detect-tempo.txt"
code=$?
set -e
# 0 = limpo, 2 = achados; outros códigos são falha
if [[ $code -ne 0 && $code -ne 2 ]]; then
  echo "detect falhou com código $code" >&2
  cat "$ROOT/detect-tempo.txt" >&2
  exit $code
fi
cat "$ROOT/detect-tempo.txt"
echo "detect_exit=$code"
echo "--- saida ---"
cat "$ROOT/detect-saida.json"
