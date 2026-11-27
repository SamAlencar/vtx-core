#!/usr/bin/env bash
# Teste ao vivo de RLS e grants da migração acoes_pendentes.
# Sobe um cluster Postgres temporário (não usa a porta 5432 nem o data
# dir da Evolution). Opcional no CI: rode à mão quando houver initdb.
#
# Variáveis opcionais:
#   PG_BIN  diretório com initdb e pg_ctl (senão: PATH, depois `pg_config --bindir`)
#   PSQL    cliente psql (senão: PATH, ou $PG_BIN/psql)
#   DADOS   data dir temporário (padrão: /workspace/pg-acoes-rls-tmp, ou mktemp).
#          Só aceita /workspace/<subdir> ou ${TMPDIR:-/tmp}/pg-acoes-*; recusa vazio, / e o resto.
#   PORTA   porta de escuta (padrão: 55432; recusa 5432)
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
  echo "teste-rls-acoes: initdb e pg_ctl não estão no PATH." >&2
  echo "  Defina PG_BIN para o diretório dos binários do Postgres (o que contém initdb e pg_ctl)," >&2
  echo "  ou instale o servidor e deixe initdb/pg_ctl no PATH, ou tenha pg_config --bindir acessível." >&2
  exit 2
fi
if [[ -z "${PSQL:-}" ]]; then
  if resolver_binario psql >/dev/null; then
    PSQL="$(resolver_binario psql)"
  else
    echo "teste-rls-acoes: psql não está no PATH. Defina PSQL ou PG_BIN." >&2
    exit 2
  fi
fi

NOME="teste-rls-acoes"

# DADOS só pode ser um subdir de /workspace/ ou ${TMPDIR:-/tmp}/pg-acoes-*.
# Recusa vazio, /, ou caminho que (depois de resolver '..') saia desses prefixos.
validar_dados() {
  local bruto="${1-}"
  if [[ -z "$bruto" || "$bruto" == "/" ]]; then
    echo "$NOME: recuso DADOS vazio ou /." >&2
    exit 2
  fi
  local canon
  canon="$(realpath -m -- "$bruto")" || {
    echo "$NOME: não consegui normalizar DADOS." >&2
    exit 2
  }
  if [[ -z "$canon" || "$canon" == "/" ]]; then
    echo "$NOME: recuso DADOS vazio ou /." >&2
    exit 2
  fi
  if [[ "$canon" == *evolution-pgdata* ]]; then
    echo "$NOME: recuso usar o data dir da Evolution." >&2
    exit 2
  fi
  local tmp
  tmp="$(realpath -m -- "${TMPDIR:-/tmp}")"
  if [[ "$canon" == /workspace/* ]]; then
    DADOS="$canon"
    return 0
  fi
  if [[ "$canon" == "$tmp"/pg-acoes-* ]]; then
    DADOS="$canon"
    return 0
  fi
  echo "$NOME: recuso DADOS fora de /workspace/ ou ${tmp}/pg-acoes-*: $canon" >&2
  exit 2
}

remover_dados() {
  validar_dados "$DADOS"
  rm -rf -- "$DADOS"
}

if [[ -d /workspace ]]; then
  DADOS="${DADOS:-/workspace/pg-acoes-rls-tmp}"
else
  DADOS="${DADOS:-$(mktemp -d "${TMPDIR:-/tmp}/pg-acoes-rls.XXXXXX")}"
fi
PORTA="${PORTA:-55432}"
validar_dados "$DADOS"
LOG="$DADOS/postgres.log"
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
    "$PGCTL" -D "$DADOS" -w stop -m fast >/dev/null 2>&1 || true
  fi
  remover_dados
}
trap derrubar EXIT

remover_dados
"$INITDB" -D "$DADOS" -E UTF8 --locale=C --no-sync --auth=trust --username=postgres >/dev/null
cat >> "$DADOS/postgresql.conf" << EOF
listen_addresses = '127.0.0.1'
port = $PORTA
unix_socket_directories = '$DADOS'
logging_collector = off
EOF

"$PGCTL" -D "$DADOS" -w start -l "$LOG" >/dev/null

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


como_anon() {
  psqlq -tA << SQL
\\set QUIET on
set role anon;
\\set QUIET off
$1
SQL
}

# 9. Dono lê só a própria auditoria.
if saida=$(como_autenticado "$USUARIO_A" "select count(*) || '|' || string_agg(evento, ',' order by em, id) from public.acoes_auditoria;"); then
  if [[ "$saida" == "3|criada,aprovada,executada" ]]; then
    ok "dono lê só a própria auditoria (criada, aprovada, executada)"
  else
    falhou "auditoria do dono deveria ser 3|criada,aprovada,executada, veio: $saida"
  fi
else
  falhou "select em acoes_auditoria como dono"
fi

# 10. Outro usuário não vê a auditoria do dono.
if saida=$(como_autenticado "$USUARIO_B" "select count(*) from public.acoes_auditoria;"); then
  if [[ "$saida" == "0" ]]; then
    ok "outro usuário não vê a auditoria do dono"
  else
    falhou "usuário B viu auditoria count=$saida (deveria ser 0)"
  fi
else
  falhou "select de auditoria do usuário B falhou"
fi

# 11. Authenticated não insere, atualiza nem apaga auditoria.
set +e
saida=$(como_autenticado "$USUARIO_A" "insert into public.acoes_auditoria (acao_id, usuario_id, evento) values ('$ACAO', '$USUARIO_A', 'aprovada');" 2>&1)
rc=$?
set -e
if [[ $rc -ne 0 ]] && echo "$saida" | grep -qi 'permission denied'; then
  ok "authenticated não insere auditoria"
else
  falhou "insert em acoes_auditoria deveria ser negado, veio (rc=$rc): $saida"
fi

set +e
saida=$(como_autenticado "$USUARIO_A" "update public.acoes_auditoria set evento = 'executada' where acao_id = '$ACAO';" 2>&1)
rc=$?
set -e
if [[ $rc -ne 0 ]] && echo "$saida" | grep -qi 'permission denied'; then
  ok "authenticated não atualiza auditoria"
else
  falhou "update em acoes_auditoria deveria ser negado, veio (rc=$rc): $saida"
fi

set +e
saida=$(como_autenticado "$USUARIO_A" "delete from public.acoes_auditoria where acao_id = '$ACAO';" 2>&1)
rc=$?
set -e
if [[ $rc -ne 0 ]] && echo "$saida" | grep -qi 'permission denied'; then
  ok "authenticated não apaga auditoria"
else
  falhou "delete em acoes_auditoria deveria ser negado, veio (rc=$rc): $saida"
fi

# 12. anon não lê ações, view nem auditoria.
for alvo in public.acoes_pendentes public.acoes_pendentes_leitura public.acoes_auditoria; do
  set +e
  saida=$(como_anon "select count(*) from $alvo;" 2>&1)
  rc=$?
  set -e
  if [[ $rc -ne 0 ]] && echo "$saida" | grep -qi 'permission denied'; then
    ok "anon não lê $alvo"
  else
    falhou "anon deveria ter permission denied em $alvo, veio (rc=$rc): $saida"
  fi
done

if [[ "$falhas" -ne 0 ]]; then
  echo "teste-rls-acoes: $falhas falha(s)" >&2
  exit 1
fi
echo "teste-rls-acoes: todas as provas passaram (cluster temporário na porta $PORTA)."
