#!/usr/bin/env bash
# Teste ao vivo: RPCs que retornam composto `return null` chegam como linha
# com todas as colunas nulas (formato PostgREST), e o cliente trata isso
# como ausência. Segue o padrão de teste-rls-acoes.sh.
#
# Sobe um cluster Postgres temporário (não usa a porta 5432 nem o data
# dir da Evolution). Opcional no CI.
#
# Variáveis opcionais:
#   PG_BIN  diretório com initdb e pg_ctl
#   PSQL    cliente psql
#   DADOS   data dir temporário (padrão: /workspace/pg-acoes-rpc-nulo-tmp)
#   PORTA   porta de escuta (padrão: 55433; recusa 5432)
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
MIGRACAO="$RAIZ/supabase/migrations/20261127000000_acoes_pendentes.sql"

resolver_binario() {
  local nome="$1"
  if command -v "$nome" >/dev/null 2>&1; then
    command -v "$nome"
    return 0
  fi
  if [[ -n "${PG_BIN:-}" && -x "$PG_BIN/$nome" ]]; then
    echo "$PG_BIN/$nome"
    return 0
  fi
  return 1
}

if [[ -z "${PG_BIN:-}" ]]; then
  if command -v pg_config >/dev/null 2>&1; then
    PG_BIN="$(pg_config --bindir)"
  fi
fi
if [[ -n "${PG_BIN:-}" ]]; then
  export PATH="$PG_BIN:$PATH"
fi

INITDB="$(resolver_binario initdb || true)"
PGCTL="$(resolver_binario pg_ctl || true)"
if [[ -z "$INITDB" || -z "$PGCTL" ]]; then
  echo "teste-rpc-acoes-composto-nulo: initdb e pg_ctl não estão no PATH." >&2
  echo "  Defina PG_BIN para o diretório dos binários do Postgres." >&2
  exit 2
fi
if [[ -z "${PSQL:-}" ]]; then
  if resolver_binario psql >/dev/null; then
    PSQL="$(resolver_binario psql)"
  else
    echo "teste-rpc-acoes-composto-nulo: psql não está no PATH. Defina PSQL ou PG_BIN." >&2
    exit 2
  fi
fi

if [[ -d /workspace ]]; then
  DADOS="${DADOS:-/workspace/pg-acoes-rpc-nulo-tmp}"
else
  DADOS="${DADOS:-$(mktemp -d "${TMPDIR:-/tmp}/pg-acoes-rpc-nulo.XXXXXX")}"
fi
PORTA="${PORTA:-55433}"
LOG="$DADOS/postgres.log"
if [[ ! -f "$MIGRACAO" ]]; then
  echo "teste-rpc-acoes-composto-nulo: migração não encontrada: $MIGRACAO" >&2
  exit 2
fi
if [[ "$DADOS" == *evolution-pgdata* ]]; then
  echo "teste-rpc-acoes-composto-nulo: recuso usar o data dir da Evolution" >&2
  exit 2
fi
if [[ "$PORTA" == "5432" ]]; then
  echo "teste-rpc-acoes-composto-nulo: recuso a porta 5432 (Evolution)" >&2
  exit 2
fi

derrubar() {
  if [[ -d "$DADOS" && -f "$DADOS/postmaster.pid" ]]; then
    "$PGCTL" -D "$DADOS" -w stop -m fast >/dev/null 2>&1 || true
  fi
  rm -rf "$DADOS"
}
trap derrubar EXIT

rm -rf "$DADOS"
"$INITDB" -D "$DADOS" -E UTF8 --locale=C --no-sync --auth=trust --username=postgres >/dev/null
cat >> "$DADOS/postgresql.conf" << PGEOF
listen_addresses = '127.0.0.1'
port = $PORTA
unix_socket_directories = '$DADOS'
logging_collector = off
PGEOF

"$PGCTL" -D "$DADOS" -w start -l "$LOG" >/dev/null

psqlq() {
  "$PSQL" -h 127.0.0.1 -p "$PORTA" -U postgres -d postgres -v ON_ERROR_STOP=1 --no-psqlrc "$@"
}

psqlq -q << 'SQL'
create schema if not exists auth;

create table auth.users (
  id uuid primary key
);

create or replace function auth.uid()
returns uuid
language sql
stable
as $$
  select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid
$$;

do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'anon') then
    create role anon nologin;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'authenticated') then
    create role authenticated nologin;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'service_role') then
    create role service_role nologin bypassrls;
  else
    alter role service_role bypassrls;
  end if;
end
$$;

grant usage on schema public to anon, authenticated, service_role;
grant usage on schema auth to authenticated, service_role;
grant execute on function auth.uid() to anon, authenticated, service_role;
SQL

psqlq -q -f "$MIGRACAO" >/dev/null

USUARIO_A='11111111-1111-4111-8111-111111111111'
USUARIO_B='22222222-2222-4222-8222-222222222222'
ACAO_PENDENTE='33333333-3333-4333-8333-333333333333'
ACAO_EXPIRADA='44444444-4444-4444-8444-444444444444'
ACAO_ALHEIA='55555555-5555-4555-8555-555555555555'
TRACE='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'

psqlq -q << SQL
insert into auth.users (id) values ('$USUARIO_A'), ('$USUARIO_B');

do \$\$
begin
  perform public.acoes_criar(
    '$ACAO_PENDENTE'::uuid,
    '$USUARIO_A'::uuid,
    'pagar',
    '{"valor": 50}'::jsonb,
    '$TRACE'::uuid,
    now(),
    now() + interval '1 day',
    null
  );
  perform public.acoes_criar(
    '$ACAO_EXPIRADA'::uuid,
    '$USUARIO_A'::uuid,
    'pagar',
    '{"valor": 1}'::jsonb,
    '$TRACE'::uuid,
    now() - interval '2 days',
    now() - interval '1 day',
    null
  );
  perform public.acoes_criar(
    '$ACAO_ALHEIA'::uuid,
    '$USUARIO_A'::uuid,
    'pagar',
    '{"valor": 2}'::jsonb,
    '$TRACE'::uuid,
    now(),
    now() + interval '1 day',
    null
  );
end
\$\$;
SQL

falhas=0
ok() { echo "  ok: $1"; }
falhou() { echo "  FALHOU: $1" >&2; falhas=$((falhas + 1)); }

como_service() {
  psqlq -tA << SQL
\\set QUIET on
set role service_role;
\\set QUIET off
$1
SQL
}

# 1. return null numa função composta gera 1 linha, não zero.
if saida=$(como_service "select count(*) from public.acoes_reivindicar('$ACAO_EXPIRADA'::uuid, '$USUARIO_A'::uuid, now(), interval '40 seconds');"); then
  if [[ "$saida" == "1" ]]; then
    ok "acoes_reivindicar com return null devolve 1 linha (não zero)"
  else
    falhou "count(*) de reivindicar expirada deveria ser 1, veio: $saida"
  fi
else
  falhou "count(*) de reivindicar expirada falhou: $saida"
fi

# 2. Essa linha tem id nulo (formato que o PostgREST entrega).
if saida=$(como_service "select row_to_json(t) from public.acoes_reivindicar('$ACAO_ALHEIA'::uuid, '$USUARIO_B'::uuid, now(), interval '40 seconds') t;"); then
  if echo "$saida" | grep -q '"id":null' && echo "$saida" | grep -q '"tool":null'; then
    ok "a linha composta nula tem id e tool nulos (formato PostgREST)"
    printf '%s\n' "$saida" > "$DADOS/composto-nulo.json"
  else
    falhou "esperava json com id/tool null, veio: $saida"
  fi
else
  falhou "row_to_json de reivindicar de outro usuário falhou: $saida"
fi

# 3. Rejeitar já decidida também devolve composto nulo (depois de rejeitar de verdade).
if saida=$(como_service "select (public.acoes_rejeitar('$ACAO_PENDENTE'::uuid, '$USUARIO_A'::uuid, now())).status;
select row_to_json(t) from public.acoes_rejeitar('$ACAO_PENDENTE'::uuid, '$USUARIO_A'::uuid, now()) t;"); then
  if echo "$saida" | grep -q rejeitada && echo "$saida" | grep -q '"id":null'; then
    ok "segunda rejeição devolve composto nulo; a primeira gravou rejeitada"
    printf '%s\n' "$saida" | tail -n 1 > "$DADOS/composto-nulo-rejeitar.json"
  else
    falhou "rejeitar duas vezes deveria ser rejeitada + id null, veio: $saida"
  fi
else
  falhou "rejeitar duas vezes falhou: $saida"
fi

# 4. O cliente TypeScript trata o json composto nulo como ausência e cobre o fluxo ao vivo.
export PSQL
export PGHOST=127.0.0.1
export PGPORT="$PORTA"
export PGUSER=postgres
export PGDATABASE=postgres
export ACOES_RPC_LIVE=1
export ACOES_RPC_NULO_JSON="$DADOS/composto-nulo.json"
export ACOES_RPC_NULO_REJEITAR_JSON="$DADOS/composto-nulo-rejeitar.json"

set +e
saida=$(
  cd "$RAIZ" && npm_config_audit=false npm_config_fund=false \
    npx vitest run --config vitest.config.mts tests/integracao/acoes-rpc-composto-nulo.live.test.ts 2>&1
)
rc=$?
set -e
if [[ $rc -eq 0 ]]; then
  ok "cliente TypeScript trata o composto nulo e o fluxo ao vivo"
else
  falhou "vitest ao vivo falhou (rc=$rc): $saida"
fi

if [[ "$falhas" -ne 0 ]]; then
  echo "teste-rpc-acoes-composto-nulo: $falhas falha(s)" >&2
  exit 1
fi
echo "teste-rpc-acoes-composto-nulo: todas as provas passaram (cluster temporário na porta $PORTA)."
