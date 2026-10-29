# Appwrite
> Backend, BaaS e banco · Status: **avaliado, não adotado** (alternativa ao Supabase quando o cliente pedir) · Revisado em 2026-10-29 · VTX-103

## 1. O que é
Backend open source (BSD-3-Clause, v2.6.2 em 29/10/2026): Auth, banco (TablesDB; Postgres/MySQL só em compute dedicado pago), Storage, Functions, Realtime, Messaging e Sites (hospedagem). Roda no Appwrite Cloud ou em self-host com Docker. O backend padrão da VTX continua o [Supabase](supabase.md) (VTX-023).

## 2. Quando usar / quando não usar
- **Usar:** cliente que já usa ou exige Appwrite; app mobile (SDKs Flutter, Swift, Kotlin maduros); projeto que quer self-host simples num VPS.
- **Não usar:** quando precisar de SQL/RLS do Postgres no plano grátis; dado pessoal que deve ficar no Brasil (Cloud não tem região BR); produção com cliente no Free.

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Supabase | padrão VTX | Postgres + RLS, região São Paulo |
| Appwrite self-host (Docker/VPS) | dado no Brasil, custo fixo | mesmo código; operação e backup por nossa conta (A2) |
| Firebase | cliente Google | ver VTX-104 |

## 4. Custo e plano gratuito (conferido em 29/10/2026)
- **Free, US$ 0:** 1 organização, 2 projetos (recursos compartilhados), 5 GB/mês de banda, 2 GB de arquivos (até 50 MB cada), 750 mil execuções e 100 GB-hora/mês, 75 mil usuários ativos/mês, 500 mil leituras e 250 mil escritas/mês, 1 banco, 1 bucket e 2 funções por projeto, logs de 1 hora, **sem backup**.
- **Pausa:** projeto Free sem atividade de desenvolvimento por **7 dias seguidos** é pausado (dados ficam; reativa no Console). Ao bater limite, o serviço afetado para até o próximo ciclo de 30 dias.
- **Pro:** cobrado por organização, com recursos dedicados, backup diário de 7 dias, projeto extra US$ 15 e excedentes por uso; teto de gasto (*budget cap*) disponível. **Qualquer plano pago é decisão do Samuel (A2).**

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | backend | só se o cliente pedir; senão Supabase |
| [Mobile](../../processos/fluxos/app-mobile.md) | backend | SDK nativo + Auth + Storage para fotos |
| [API](../../processos/fluxos/api-integracoes.md) | integrações | Functions para webhook (assinatura verificada) |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | demo | Free, ciente da pausa e da falta de backup |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | sistema herdado | manter Appwrite; migrar só com ADR |

## 6. Papel responsável
Arquiteto decide Appwrite x Supabase por ADR; Dev Backend modela coleções, permissões e funções; DevOps cuida de projeto, chaves, região ou self-host e backup; QA testa permissões com usuários diferentes; Samuel aprova plano pago e fornecedor com dado pessoal ([papéis](../../../agents/)).

## 7. Setup
1. Local primeiro: self-host com Docker (guia oficial) ou projeto `dev` no Cloud; CLI `appwrite` para versionar tabelas, buckets e funções (`appwrite init` / `appwrite push`).
2. Região do Cloud: escolher a mais próxima permitida pelo cliente (hoje FRA, NYC, SFO, TOR, SYD, SGP; nenhuma no Brasil).
3. SDK cliente só com o ID do projeto; SDK servidor com chave de API de escopo mínimo.
4. **MCP:** o MCP de docs do Appwrite está conectado (só leitura de documentação, fonte desta ficha); MCP de API só no projeto `dev`.

## 8. Segredos e segurança/LGPD
- Permissões por tabela/linha e por bucket em todo recurso; nunca `any` para escrita; ligar *row security* quando cada usuário só vê o que é seu.
- Chave de API só no servidor (Function, CI, variável Secret da Vercel), com escopos mínimos; nunca no app, no repositório ou no chat.
- Cloud fora do Brasil é transferência internacional de dado pessoal: registrar base legal no [desenvolvimento seguro](../../seguranca/desenvolvimento-seguro.md) ou usar self-host no Brasil (A2).
- Free sem backup: exportar dados (CLI/migração) se o projeto guardar algo que importa.

## 9. Checklist
- [ ] ADR justificando Appwrite em vez de Supabase
- [ ] Projeto `dev` separado de produção; MCP de API só no `dev`
- [ ] Permissões em todos os recursos e teste com dois usuários (QA)
- [ ] Chaves de API com escopo mínimo, só no servidor
- [ ] Região ou self-host compatível com a LGPD do cliente
- [ ] Pausa do Free e backup tratados

## 10. Registro de avaliação e Fontes
**ADR curto (29/10/2026):** *Contexto:* catálogo F12; Supabase já adotado. *Opções:* adotar Appwrite como padrão, manter como alternativa, descartar. *Decisão:* alternativa para quando o cliente pedir ou para self-host. *Consequência:* sem custo; a VTX mantém um backend padrão só.
- Preços e limites: https://appwrite.io/pricing
- Free plan e limites atingidos: https://appwrite.io/docs/advanced/billing/free
- Pausa de projetos inativos: https://appwrite.io/changelog/entry/2026-02-20-1
- Regiões: https://appwrite.io/docs/products/network/regions
- Permissões: https://appwrite.io/docs/advanced/platform/permissions
- Chaves de API: https://appwrite.io/docs/advanced/security/api-keys
- Self-host: https://appwrite.io/docs/advanced/self-hosting
- MCP: https://appwrite.io/docs/tooling/mcp
