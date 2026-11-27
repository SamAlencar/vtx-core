#!/usr/bin/env bash
# Teste ao vivo de RLS e grants da migração acoes_pendentes.
# Sobe um cluster Postgres temporário (não usa a porta 5432 nem o data
# dir da Evolution). Opcional no CI: rode à mão quando houver initdb.
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
MIGRACAO="$RAIZ/supabase/migrations/20261127000000_acoes_pendentes.sql"
PG_BIN="${PG_BIN:-/home/box/pg-local/root/usr/lib/postgresql/17/bin}"
PSQL="${PSQL:-/usr/lib/postgresql/17/bin/psql}"
# Cluster temporário sob /workspace, nunca em /home/box/evolution-pgdata.
DADOS="${DADOS:-/workspace/pg-acoes-rls-tmp}"
PORTA="${PORTA:-55432}"
LOG="$DADOS/postgres.log"
export PATH="$PG_BIN:$PATH"

if [[ ! -x "$PG_BIN/initdb" || ! -x "$PG_BIN/pg_ctl" ]]; then
  echo "teste-rls-acoes: initdb/pg_ctl não encontrados em $PG_BIN" >&2
  exit 2
fi
if [[ ! -f "$MIGRACAO" ]]; then
  echo "teste-rls-acoes: migração não encontrada: $MIGRACAO" >&2
  exit 2
fi
if [[ "$DADOS" == *evolution-pgdata* ]]; then
  echo "teste-rls-acoes: recuso usar o data dir da Evolution" >&2
  exit 2
fi
if [[ "$PORTA" == "5432" ]]; then
  echo "teste-rls-acoes: recuso a porta 5432 (Evolution)" >&2
  exit 2
fi

derrubar() {
  if [[ -d "$DADOS" && -f "$DADOS/postmaster.pid" ]]; then
    pg_ctl -D "$DADOS" -w stop -m fast >/dev/null 2>&1 || true
  fi
  rm -rf "$DADOS"
}
trap derrubar EXIT

rm -rf "$DADOS"
initdb -D "$DADOS" -E UTF8 --locale=C --no-sync --auth=trust --username=postgres >/dev/null
cat >> "$DADOS/postgresql.conf" << EOF
listen_addresses = '127.0.0.1'
port = $PORTA
unix_socket_directories = '$DADOS'
logging_collector = off
EOF

pg_ctl -D "$DADOS" -w start -l "$LOG" >/dev/null

psqlq() {
  "$PSQL" -h 127.0.0.1 -p "$PORTA" -U postgres -d postgres -v ON_ERROR_STOP=1 --no-psqlrc "$@"
}
psql_setup() {
  psqlq -q "$@"
}

# Papéis e auth.uid() no estilo Supabase, sem tocar em nenhum outro cluster.
psql_setup << 'SQL'
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

psql_setup -f "$MIGRACAO" >/dev/null

USUARIO_A='11111111-1111-4111-8111-111111111111'
USUARIO_B='22222222-2222-4222-8222-222222222222'
ACAO='33333333-3333-4333-8333-333333333333'

psql_setup << SQL
insert into auth.users (id) values ('$USUARIO_A'), ('$USUARIO_B');

do \$\$
begin
  perform public.acoes_criar(
    '$ACAO'::uuid,
    '$USUARIO_A'::uuid,
    'pagar',
    '{"valor": 50}'::jsonb,
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'::uuid,
    now(),
    now() + interval '1 day',
    jsonb_build_object('sistema', 'prompt secreto do sistema', 'mensagens', '[]'::jsonb)
  );
end
\$\$;
SQL

falhas=0
ok() { echo "  ok: $1"; }
falhou() { echo "  FALHOU: $1" >&2; falhas=$((falhas + 1)); }

# Uma sessão: setup quieto (role + uid) + um comando. ON_ERROR_STOP no psqlq.
sessao() {
  local uid="$1"
  local corpo="$2"
  psqlq -tA << SQL
\\set QUIET on
set role $3;
do \$\$ begin perform set_config('request.jwt.claim.sub', '$uid', false); end \$\$;
\\set QUIET off
$corpo
SQL
}

como_autenticado() { sessao "$1" "$2" authenticated; }
como_service() {
  psqlq -tA << SQL
\\set QUIET on
set role service_role;
\\set QUIET off
$1
SQL
}

# 1. Dono lê as colunas permitidas.
if saida=$(como_autenticado "$USUARIO_A" "select tool || '|' || status from public.acoes_pendentes where id = '$ACAO';"); then
  if [[ "$saida" == *pagar\|pendente* ]]; then
    ok "dono lê as próprias linhas nas colunas permitidas"
  else
    falhou "dono deveria ver pagar|pendente, veio: $saida"
  fi
else
  falhou "select das colunas permitidas como dono (permission denied?)"
fi

# 2. Dono lê pela view (sem contexto_retomada).
if saida=$(como_autenticado "$USUARIO_A" "select tool from public.acoes_pendentes_leitura where id = '$ACAO';"); then
  if [[ "$saida" == *pagar* ]]; then
    ok "dono lê pela view acoes_pendentes_leitura"
  else
    falhou "view deveria devolver pagar, veio: $saida"
  fi
else
  falhou "select na view como authenticated"
fi

# 3. Não lê contexto_retomada (nem o prompt).
set +e
saida=$(como_autenticado "$USUARIO_A" "select contexto_retomada from public.acoes_pendentes where id = '$ACAO';" 2>&1)
rc=$?
set -e
if [[ $rc -ne 0 ]] && echo "$saida" | grep -qi 'permission denied'; then
  ok "dono não lê contexto_retomada (permission denied)"
else
  falhou "select contexto_retomada deveria ser negado, veio (rc=$rc): $saida"
fi

# 4. Outro usuário não vê as linhas (RLS).
if saida=$(como_autenticado "$USUARIO_B" "select count(*) from public.acoes_pendentes_leitura;"); then
  if [[ "$saida" == "0" ]]; then
    ok "outro usuário não vê as ações do dono"
  else
    falhou "usuário B viu count=$saida (deveria ser 0)"
  fi
else
  falhou "select do usuário B falhou: $saida"
fi

# 5. Authenticated não insere.
set +e
saida=$(como_autenticado "$USUARIO_A" "insert into public.acoes_pendentes (
  id, usuario_id, tool, input, status, trace_id, criado_em, expira_em
) values (
  '44444444-4444-4444-8444-444444444444',
  '$USUARIO_A',
  'pagar',
  '{}'::jsonb,
  'pendente',
  'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
  now(),
  now() + interval '1 day'
);" 2>&1)
rc=$?
set -e
if [[ $rc -ne 0 ]] && echo "$saida" | grep -qi 'permission denied'; then
  ok "authenticated não insere ação"
else
  falhou "insert como authenticated deveria ser negado, veio (rc=$rc): $saida"
fi

# 6. Authenticated não atualiza / não "aprova".
set +e
saida=$(como_autenticado "$USUARIO_A" "update public.acoes_pendentes set status = 'executada' where id = '$ACAO';" 2>&1)
rc=$?
set -e
if [[ $rc -ne 0 ]] && echo "$saida" | grep -qi 'permission denied'; then
  ok "authenticated não atualiza/aprova pela tabela"
else
  falhou "update como authenticated deveria ser negado, veio (rc=$rc): $saida"
fi

# 7. Authenticated não executa a RPC de reivindicar (aprovar).
set +e
saida=$(como_autenticado "$USUARIO_A" "select public.acoes_reivindicar('$ACAO'::uuid, '$USUARIO_A'::uuid, now());" 2>&1)
rc=$?
set -e
if [[ $rc -ne 0 ]] && echo "$saida" | grep -qi 'permission denied'; then
  ok "authenticated não chama acoes_reivindicar"
else
  falhou "acoes_reivindicar como authenticated deveria ser negado, veio (rc=$rc): $saida"
fi

# 8. service_role executa as RPCs.
if saida=$(como_service "select status from public.acoes_reivindicar('$ACAO'::uuid, '$USUARIO_A'::uuid, now(), interval '40 seconds');
select status from public.acoes_concluir('$ACAO'::uuid, 'executada', '{\"ok\": true}'::jsonb, null);"); then
  if echo "$saida" | grep -q executando && echo "$saida" | grep -q executada; then
    ok "service_role executa acoes_reivindicar e acoes_concluir"
  else
    falhou "RPCs como service_role devolveram: $saida"
  fi
else
  falhou "service_role deveria executar as RPCs: $saida"
fi

if [[ "$falhas" -ne 0 ]]; then
  echo "teste-rls-acoes: $falhas falha(s)" >&2
  exit 1
fi
echo "teste-rls-acoes: todas as provas passaram (cluster temporário na porta $PORTA)."
