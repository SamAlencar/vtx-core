# Modelagem de dados e bancos de dados

> VTX-025 · Fase F4 · Base de Conhecimento. Como o **Arquiteto** e o **Dev Backend** ([dev-backend.md](../../agents/dev-backend.md)) modelam, migram e protegem dados no Postgres do Supabase, padrão do [stack de referência](stack-de-referencia.md). Contratos de API: [design de APIs](design-de-apis.md).

## 1. Conceitos
- **Modelo conceitual → lógico → físico:** entidades e regras do domínio (vindas do [DDD](../engenharia/padroes-de-projeto-ddd.md)) → tabelas e relações → tipos, índices e políticas no Postgres.
- **Normalizar até a 3FN** (cada fato num lugar só) e desnormalizar só com motivo medido (relatório lento), registrado em ADR.
- **Relacional por padrão;** `jsonb` só para dado sem esquema fixo (respostas de formulário, payload de webhook), nunca para algo que se filtra ou relaciona sempre.
- **RLS (Row Level Security):** a política no banco é a última barreira; vale mesmo se o código errar. Obrigatória em toda tabela do schema `public`.
- **Migração versionada:** todo esquema muda por arquivo SQL em `supabase/migrations/`, revisado em PR e aplicado pelo CI; nunca editar pelo painel em produção.

## 2. Metodologia
1. **Listar entidades e regras** a partir do PRD: identificador, atributos, cardinalidade, quem pode ler/alterar e se há **dado pessoal** (LGPD: finalidade, base legal, prazo de retenção).
2. **Desenhar o diagrama ER** em Mermaid (`erDiagram`) no `docs/` do projeto e revisar com o Arquiteto.
3. **Aplicar as convenções:**
   - nomes em `snake_case`, tabela no plural (`projetos`), chave `id uuid default gen_random_uuid()`;
   - FK `<entidade>_id` com `references` e `on delete` explícito; índice em toda FK e coluna filtrada;
   - `created_at`/`updated_at timestamptz default now()`; datas sempre `timestamptz` (UTC);
   - dinheiro em `bigint` centavos ou `numeric(12,2)`, nunca `float`; status em `text` + `check` (ou enum se estável);
   - restrições no banco (`not null`, `unique`, `check`), não só no código; dono do registro em `owner_id uuid references auth.users`.
4. **Escrever as políticas RLS** junto com a tabela, na mesma migração, e testar com dois usuários (A não lê B).
5. **Gerar tipos** (`supabase gen types typescript`) para `packages/shared` e alinhar com os schemas Zod.
6. **Mudar sem quebrar (expand-contract):** adicionar coluna/tabela nova → copiar dados e passar o código → só depois remover a antiga, em outra migração. Coluna nova em tabela grande: nullable ou com default.
7. **Desempenho:** `explain analyze` nas consultas principais; índice para cada filtro/ordenação frequente; paginação por cursor; conexão pelo pooler do Supabase em funções serverless.
8. **Proteger os dados:** backup diário do Supabase (plano Free tem limites, anotar no PRD), dump antes de migração arriscada, `service_role` só no servidor, dado pessoal mínimo e com rotina de exclusão no fim do prazo.

## 3. Exemplo
```sql
-- supabase/migrations/20261025120000_projetos.sql
create table public.projetos (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users on delete cascade,
  nome text not null check (char_length(nome) between 3 and 120),
  status text not null default 'rascunho' check (status in ('rascunho','em_revisao','aprovado')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index projetos_owner_id_idx on public.projetos (owner_id);
alter table public.projetos enable row level security;
create policy "dono lê e altera" on public.projetos
  for all using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);
```
O `(select auth.uid())` faz o Postgres avaliar a função uma vez por consulta, e não por linha.

## 4. Checklist da migração
- [ ] Diagrama ER atualizado; cada tabela com dono, finalidade e (se pessoal) prazo de retenção.
- [ ] Convenções de nomes, `uuid`, `timestamptz`, dinheiro sem `float`, restrições no banco.
- [ ] RLS ligada e políticas testadas com dois usuários; `service_role` fora do cliente.
- [ ] Índice nas FKs e nos filtros principais; `explain analyze` nas consultas críticas.
- [ ] Migração reversível ou expand-contract; nenhuma remoção na mesma migração que adiciona.
- [ ] Tipos regenerados e schemas Zod alinhados; `supabase db reset` local passa.
- [ ] Mudança em produção aprovada conforme [governança](../processos/governanca-e-aprovacoes.md).

## 5. Fontes
- PostgreSQL — Data Definition: https://www.postgresql.org/docs/current/ddl.html
- PostgreSQL — Using EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- Supabase — Row Level Security: https://supabase.com/docs/guides/database/postgres/row-level-security
- Supabase — Database migrations: https://supabase.com/docs/guides/deployment/database-migrations
- Supabase — Generating TypeScript types: https://supabase.com/docs/guides/api/rest/generating-types
- Mermaid — Entity Relationship Diagrams: https://mermaid.js.org/syntax/entityRelationshipDiagram.html
- Supabase Postgres Best Practices (skill local `supabase-postgres-best-practices`).
- LGPD (Lei 13.709/2018): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
