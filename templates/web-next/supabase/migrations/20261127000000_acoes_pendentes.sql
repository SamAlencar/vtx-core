-- VTX-213: ações pendentes de tools críticas e auditoria.
-- Escrita só no servidor: service_role (bypassa RLS) ou RPC security definer
-- com search_path fixo e EXECUTE só para service_role.
-- O papel authenticated só faz SELECT das próprias linhas. Sem isso, um
-- usuário inseriria uma ação pendente pelo PostgREST e a "aprovaria" com
-- input arbitrário, forjando também a auditoria.

create table if not exists public.acoes_pendentes (
  id uuid primary key,
  usuario_id uuid not null references auth.users (id) on delete cascade,
  tool text not null,
  input jsonb not null,
  status text not null default 'pendente'
    check (status in (
      'pendente', 'executando', 'executada', 'falhou', 'rejeitada', 'expirada'
    )),
  trace_id uuid not null,
  criado_em timestamptz not null default now(),
  expira_em timestamptz not null,
  executando_em timestamptz,
  contexto_retomada jsonb,
  aprovado_por uuid references auth.users (id),
  aprovado_em timestamptz,
  resultado jsonb,
  erro text
);

create index if not exists acoes_pendentes_usuario_idx on public.acoes_pendentes (usuario_id);

alter table public.acoes_pendentes enable row level security;

create policy acoes_pendentes_select on public.acoes_pendentes
  for select to authenticated
  using (usuario_id = (select auth.uid()));

revoke all on table public.acoes_pendentes from public, anon, authenticated;
-- Sem GRANT SELECT na tabela: contexto_retomada (prompt de sistema e
-- histórico) não vaza pelo PostgREST. A leitura do usuário vai pela view.
grant all on table public.acoes_pendentes to service_role;

create or replace view public.acoes_pendentes_leitura
  with (security_invoker = true)
  as select
    id,
    usuario_id,
    tool,
    input,
    status,
    trace_id,
    criado_em,
    expira_em,
    executando_em,
    aprovado_por,
    aprovado_em,
    resultado,
    erro
  from public.acoes_pendentes;

revoke all on public.acoes_pendentes_leitura from public, anon;
grant select on public.acoes_pendentes_leitura to authenticated;

create table if not exists public.acoes_auditoria (
  id bigint generated always as identity primary key,
  acao_id uuid not null references public.acoes_pendentes (id) on delete cascade,
  usuario_id uuid not null references auth.users (id) on delete cascade,
  evento text not null check (evento in (
    'criada', 'aprovada', 'executada', 'falhou', 'rejeitada', 'expirada'
  )),
  em timestamptz not null default now()
);

create index if not exists acoes_auditoria_acao_idx on public.acoes_auditoria (acao_id);

alter table public.acoes_auditoria enable row level security;

create policy acoes_auditoria_select on public.acoes_auditoria
  for select to authenticated
  using (usuario_id = (select auth.uid()));

revoke all on table public.acoes_auditoria from public, anon, authenticated;
grant select on table public.acoes_auditoria to authenticated;
grant all on table public.acoes_auditoria to service_role;
grant usage, select on sequence public.acoes_auditoria_id_seq to service_role;

-- RPCs de escrita: security definer, search_path fixo, grants mínimos.
-- acoes_reivindicar e acoes_concluir auditam aprovada/executada/falhou;
-- o repositório não deve chamar acoes_auditar de novo nesses caminhos.
-- p_lease deve ser timeout da tool + margem (leaseMsDeTimeout); o padrão
-- de 40s só cobre AGENT_TIMEOUT_MS=30s + 10s de folga.
-- O servidor autentica o usuário e passa o id; as funções não usam auth.uid()
-- porque o service_role não carrega o JWT do usuário.

create or replace function public.acoes_auditar(
  p_acao_id uuid,
  p_usuario_id uuid,
  p_evento text,
  p_em timestamptz
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, public
as $$
begin
  insert into public.acoes_auditoria (acao_id, usuario_id, evento, em)
  values (p_acao_id, p_usuario_id, p_evento, p_em);
end;
$$;

create or replace function public.acoes_criar(
  p_id uuid,
  p_usuario_id uuid,
  p_tool text,
  p_input jsonb,
  p_trace_id uuid,
  p_em timestamptz,
  p_expira_em timestamptz,
  p_contexto_retomada jsonb default null
)
returns public.acoes_pendentes
language plpgsql
security definer
set search_path = pg_catalog, public
as $$
declare
  a public.acoes_pendentes;
begin
  insert into public.acoes_pendentes (
    id, usuario_id, tool, input, status, trace_id, criado_em, expira_em, contexto_retomada
  ) values (
    p_id, p_usuario_id, p_tool, p_input, 'pendente', p_trace_id, p_em, p_expira_em, p_contexto_retomada
  )
  returning * into a;
  perform public.acoes_auditar(p_id, p_usuario_id, 'criada', p_em);
  return a;
end;
$$;

create or replace function public.acoes_reivindicar(
  p_id uuid,
  p_usuario_id uuid,
  p_em timestamptz,
  p_lease interval default interval '40 seconds'
)
returns public.acoes_pendentes
language plpgsql
security definer
set search_path = pg_catalog, public
as $$
declare
  a public.acoes_pendentes;
begin
  select * into a
  from public.acoes_pendentes
  where id = p_id and usuario_id = p_usuario_id
  for update;
  if not found then
    return null;
  end if;

  if a.status = 'pendente' and a.expira_em <= p_em then
    update public.acoes_pendentes
      set status = 'expirada'
      where id = p_id
      returning * into a;
    perform public.acoes_auditar(p_id, p_usuario_id, 'expirada', p_em);
    return null;
  end if;

  if a.status = 'pendente' then
    update public.acoes_pendentes
      set status = 'executando',
          aprovado_por = p_usuario_id,
          aprovado_em = p_em,
          executando_em = p_em
      where id = p_id
      returning * into a;
    perform public.acoes_auditar(p_id, p_usuario_id, 'aprovada', p_em);
    return a;
  end if;

  if a.status = 'executando'
     and a.executando_em is not null
     and a.executando_em + p_lease <= p_em then
    update public.acoes_pendentes
      set status = 'falhou',
          erro = 'execução interrompida (timeout da reivindicação)'
      where id = p_id
      returning * into a;
    perform public.acoes_auditar(p_id, p_usuario_id, 'falhou', p_em);
    return null;
  end if;

  return null;
end;
$$;

create or replace function public.acoes_concluir(
  p_id uuid,
  p_status text,
  p_resultado jsonb default null,
  p_erro text default null
)
returns public.acoes_pendentes
language plpgsql
security definer
set search_path = pg_catalog, public
as $$
declare
  a public.acoes_pendentes;
begin
  if p_status not in ('executada', 'falhou') then
    raise exception 'desfecho inválido: %', p_status;
  end if;
  update public.acoes_pendentes
    set status = p_status,
        resultado = case when p_status = 'executada' then p_resultado else resultado end,
        erro = case when p_status = 'falhou' then p_erro else erro end
    where id = p_id and status = 'executando'
    returning * into a;
  if not found then
    raise exception 'ação % não está em executando', p_id;
  end if;
  perform public.acoes_auditar(p_id, a.usuario_id, p_status, clock_timestamp());
  return a;
end;
$$;

create or replace function public.acoes_rejeitar(
  p_id uuid,
  p_usuario_id uuid,
  p_em timestamptz
)
returns public.acoes_pendentes
language plpgsql
security definer
set search_path = pg_catalog, public
as $$
declare
  a public.acoes_pendentes;
begin
  select * into a
  from public.acoes_pendentes
  where id = p_id and usuario_id = p_usuario_id
  for update;
  if not found then
    return null;
  end if;

  if a.status = 'pendente' and a.expira_em <= p_em then
    update public.acoes_pendentes
      set status = 'expirada'
      where id = p_id
      returning * into a;
    perform public.acoes_auditar(p_id, p_usuario_id, 'expirada', p_em);
    return null;
  end if;

  if a.status <> 'pendente' then
    return null;
  end if;

  update public.acoes_pendentes
    set status = 'rejeitada'
    where id = p_id
    returning * into a;
  perform public.acoes_auditar(p_id, p_usuario_id, 'rejeitada', p_em);
  return a;
end;
$$;

revoke all on function public.acoes_auditar(uuid, uuid, text, timestamptz) from public, anon, authenticated;
revoke all on function public.acoes_criar(uuid, uuid, text, jsonb, uuid, timestamptz, timestamptz, jsonb) from public, anon, authenticated;
revoke all on function public.acoes_reivindicar(uuid, uuid, timestamptz, interval) from public, anon, authenticated;
revoke all on function public.acoes_concluir(uuid, text, jsonb, text) from public, anon, authenticated;
revoke all on function public.acoes_rejeitar(uuid, uuid, timestamptz) from public, anon, authenticated;

grant execute on function public.acoes_auditar(uuid, uuid, text, timestamptz) to service_role;
grant execute on function public.acoes_criar(uuid, uuid, text, jsonb, uuid, timestamptz, timestamptz, jsonb) to service_role;
grant execute on function public.acoes_reivindicar(uuid, uuid, timestamptz, interval) to service_role;
grant execute on function public.acoes_concluir(uuid, text, jsonb, text) to service_role;
grant execute on function public.acoes_rejeitar(uuid, uuid, timestamptz) to service_role;
