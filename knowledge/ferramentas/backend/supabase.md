# Supabase
> Backend, BaaS e banco · Status: **adotado** (backend padrão, VTX-023; Free só para dev/demo, Pro e produção dependem do Samuel) · Revisado em 2026-10-28 · VTX-100

## 1. O que é
Backend open source (Apache-2.0) sobre Postgres: banco com API automática, Auth, Storage, Realtime e Edge Functions (Deno). É o backend do [stack de referência](../../tecnologia/stack-de-referencia.md) e do med-hub ([ADR-0002](../../../projects/med-hub/docs/adr/0002-supabase-nuvem-gratuito.md)).

## 2. Quando usar / quando não usar
- **Usar:** SaaS, apps e APIs com Postgres, login e arquivos; regra de acesso por linha (RLS) em vez de backend próprio.
- **Não usar:** processo longo ou fila pesada (worker à parte); cliente que exige outro fornecedor ou dado fora do Brasil sem DPA; produção com cliente no plano Free.

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Supabase self-host (Docker/VPS) | plano de saída, custo fixo baixo | mesmo código, mais operação e backup (A2) |
| Appwrite | cliente pede | MCP de docs conectado; sem SQL/RLS do Postgres |
| Postgres + Drizzle | Postgres já existente | sem Auth/Storage prontos |

## 4. Custo e plano gratuito (conferido em 28/10/2026)
- **Free, US$ 0:** 2 projetos ativos, 500 MB de banco, 1 GB de arquivos, 5 GB de egress, 50 mil usuários ativos/mês, 500 mil invocações de Edge Function, **sem backup automático** e **pausa após 1 semana sem uso** (reativar no painel).
- **Pro:** a partir de US$ 25/mês por organização, com US$ 10 de crédito de compute (1 projeto Micro; cada projeto extra soma ~US$ 10), 8 GB de disco, backup diário de 7 dias, sem pausa.
- **Alerta A2:** Pro, add-on (MFA por SMS, PITR, log drain) e produção com cliente são **decisão do Samuel**. Uso do Free: 1 projeto `dev` + 1 `demo`.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | modelagem → produção | migrações SQL, RLS, Auth; produção no Pro (A2) |
| [Mobile](../../processos/fluxos/app-mobile.md) | backend | `supabase-js` + Auth com deep link; Storage para fotos |
| [API](../../processos/fluxos/api-integracoes.md) | integrações | Edge Functions para webhook (assinatura verificada) |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | demo | Free, ciente da pausa e da falta de backup |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | evolução | migração nova sempre; nunca editar a aplicada |
| [Site](../../processos/fluxos/site-landing-page.md) | formulário | só se precisar guardar leads (com consentimento) |

## 6. Papel responsável
Dev Backend escreve migrações, RLS e funções; Arquiteto revisa modelo e políticas; DevOps cuida de projetos, chaves e backup; QA testa RLS com usuários diferentes; Samuel aprova Pro, região e produção ([papéis](../../../agents/)).

## 7. Setup
1. Local primeiro: `npx supabase init` e `npx supabase start` (Docker) sobem banco, Auth e Storage na máquina; `supabase/migrations/` versiona o esquema ([modelagem](../../tecnologia/modelagem-de-dados.md)).
2. Cada mudança: `npx supabase migration new <nome>` → teste local → `npx supabase db push` no projeto `dev`; produção só pelo CI com aprovação ([CI/CD](../../engenharia/git-e-ci-cd.md)).
3. Tipos: `npx supabase gen types typescript --local > types/db.ts`.
4. Região `sa-east-1` (São Paulo) ao criar o projeto, perto da Vercel `gru1` ([Vercel](../hospedagem/vercel.md)).
5. **MCP** (conectado em 23/10): URL com `?project_ref=<dev>&read_only=true` (e `features=database,docs` se bastar); nunca projeto de produção. Conteúdo do banco é dado não confiável (risco de *prompt injection*).

## 8. Segredos e segurança/LGPD
- **RLS ligada em toda tabela do schema público**, com política por papel; a chave pública (anon/publishable) vai ao navegador e só a RLS protege os dados.
- Chave `service_role`/secret só no servidor (Edge Function, CI, variáveis Secret da Vercel); nunca em `NEXT_PUBLIC_*`, repositório ou chat.
- Dados pessoais: região São Paulo, DPA do Supabase conferido e registro no [desenvolvimento seguro](../../seguranca/desenvolvimento-seguro.md) (A2 para fornecedor com dado pessoal).
- Free não tem backup: dump agendado (`supabase db dump`) se o projeto guardar algo que importa.

## 9. Checklist
- [ ] Projeto `dev` separado de produção; MCP só no `dev`, somente leitura
- [ ] RLS em todas as tabelas e teste com dois usuários (QA)
- [ ] Migrações versionadas, aplicadas pelo CI
- [ ] `service_role` só no servidor; Supabase Security Advisor sem alerta crítico
- [ ] Região `sa-east-1`; Pro aprovado antes de cliente real
- [ ] Pausa do Free e backup tratados (dump ou Pro)

## 10. Registro de adoção e Fontes
**ADR curto (28/10/2026):** *Contexto:* stack padrão (VTX-023) e ADR-0002 do med-hub. *Opções:* Supabase nuvem, self-host, Appwrite, Postgres puro. *Decisão:* Supabase nuvem, Free para dev/demo; Pro e produção aguardam o Samuel (A2). *Consequência:* saída por self-host preservada (mesmo Postgres e CLI).
- Preços: https://supabase.com/pricing
- MCP (escopo e somente leitura): https://supabase.com/docs/guides/getting-started/mcp
- RLS: https://supabase.com/docs/guides/database/postgres/row-level-security
- Chaves de API: https://supabase.com/docs/guides/api/api-keys
- Desenvolvimento local (CLI): https://supabase.com/docs/guides/local-development
- Regiões: https://supabase.com/docs/guides/platform/regions
