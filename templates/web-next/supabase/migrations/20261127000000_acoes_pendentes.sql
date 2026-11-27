-- VTX-213: ações pendentes de tools críticas e auditoria, com RLS por usuário.

create table if not exists public.acoes_pendentes (
  id uuid primary key,
  usuario_id uuid not null references auth.users (id) on delete cascade,
  tool text not null,
  input jsonb not null,
  status text not null default 'pendente'
    check (status in ('pendente', 'executando', 'executada', 'falhou')),
  trace_id uuid not null,
  criado_em timestamptz not null default now(),
  aprovado_por uuid references auth.users (id),
  aprovado_em timestamptz,
  resultado jsonb,
  erro text
);

create index if not exists acoes_pendentes_usuario_idx on public.acoes_pendentes (usuario_id);

alter table public.acoes_pendentes enable row level security;

create policy acoes_pendentes_select on public.acoes_pendentes
  for select to authenticated using (usuario_id = auth.uid());

create policy acoes_pendentes_insert on public.acoes_pendentes
  for insert to authenticated
  with check (usuario_id = auth.uid() and status = 'pendente');

-- Reivindicar é um update condicional: where id = $1 and status = 'pendente'.
-- Quem aprova é o próprio dono; ação decidida não volta a pendente.
create policy acoes_pendentes_update on public.acoes_pendentes
  for update to authenticated
  using (usuario_id = auth.uid() and status in ('pendente', 'executando'))
  with check (usuario_id = auth.uid() and status <> 'pendente');

-- Auditoria só cresce: sem policy de update nem de delete.
create table if not exists public.acoes_auditoria (
  id bigint generated always as identity primary key,
  acao_id uuid not null references public.acoes_pendentes (id) on delete cascade,
  usuario_id uuid not null references auth.users (id) on delete cascade,
  evento text not null check (evento in ('criada', 'aprovada', 'executada', 'falhou')),
  em timestamptz not null default now()
);

create index if not exists acoes_auditoria_acao_idx on public.acoes_auditoria (acao_id);

alter table public.acoes_auditoria enable row level security;

create policy acoes_auditoria_select on public.acoes_auditoria
  for select to authenticated using (usuario_id = auth.uid());

create policy acoes_auditoria_insert on public.acoes_auditoria
  for insert to authenticated with check (usuario_id = auth.uid());
