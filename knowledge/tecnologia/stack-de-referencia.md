# Stack de referência da VTX

> VTX-023 · Fase F4 · Base de Conhecimento. O stack **padrão** que o **Arquiteto** ([arquiteto.md](../../agents/arquiteto.md)) parte em todo projeto e que Devs e DevOps assumem. O [catálogo de ferramentas](../ferramentas/README.md) ensina a **usar** cada item; aqui fica só a **escolha** e o motivo. Desviar exige ADR.

## 1. Critérios da escolha
1. **Custo zero para começar** e só ferramentas gratuitas/open source (regra do Samuel); plano pago é aprovação A2 ([governança](../processos/governanca-e-aprovacoes.md)).
2. **Um idioma só (TypeScript)** do banco à tela: menos contexto para os agentes, tipos compartilhados.
3. **Saída fácil:** SQL padrão (Postgres), Docker, Git, OpenTelemetry; nada que prenda o código ao fornecedor.
4. **Agentes produtivos:** tecnologias muito documentadas, com MCP/CLI oficial e skills já disponíveis no Cursor.
5. **Já aprovado:** Supabase (Samuel, 18/10/2026), Vercel, Supabase e Figma conectados e Stripe como pagamento principal (23/10/2026).

## 2. Stack padrão
| Camada | Padrão | Alternativa (com ADR) |
|---|---|---|
| Linguagem | TypeScript (modo `strict`), Node.js LTS | Python (dados/IA, scripts do arsenal) |
| Web | Next.js (App Router) + React | Vite + React para SPA simples; Astro para site de conteúdo |
| UI | Tailwind CSS + shadcn/ui (componentes copiados, MIT) | — |
| Mobile | Expo (React Native) | PWA se não precisar de loja |
| Backend / dados | Supabase: Postgres + Auth + Storage + Edge Functions, RLS obrigatória | Supabase self-host (Docker/VPS) como saída; Appwrite/Firebase só por exigência do cliente |
| Acesso a dados | `supabase-js` + tipos gerados (`supabase gen types`); SQL nas migrações | Drizzle ORM se houver Postgres fora do Supabase |
| Validação | Zod nas bordas (formulários, API, webhooks) | — |
| Pagamentos | Stripe (Checkout hospedado + webhooks), ver [pagamentos](../engenharia/pagamentos.md) | Mercado Pago quando o cliente exigir |
| Hospedagem web | Vercel (preview por PR; produção por tag) | Cloudflare Pages; VPS + Docker |
| Testes | Vitest + Testing Library, Playwright + axe-core ([testes](../engenharia/testes-e-qualidade.md)) | Jest no React Native |
| CI/CD | GitHub Actions ([Git e CI/CD](../engenharia/git-e-ci-cd.md)) | — |
| Observabilidade | Logs JSON (pino) + OpenTelemetry + logs nativos ([observabilidade](../operacao/observabilidade.md)) | Grafana OSS / GlitchTip self-host |
| Segurança no CI | gitleaks, Semgrep CE, OSV-Scanner ([segurança](../seguranca/desenvolvimento-seguro.md)) | — |
| Design | Figma (conectado) → tokens no Tailwind | — |
| IA no produto | Vercel AI SDK (troca de provedor sem reescrever) | SDK direto do provedor |
| Qualidade de código | ESLint + Prettier, `pnpm` como gerenciador | — |

## 3. Quando desviar
- **O cliente já tem stack** (sistema legado, TI própria) ou exige um fornecedor: seguir o cliente e registrar ADR.
- **Requisito que o padrão não atende** (tempo real pesado, processamento longo, dados fora do Brasil proibidos, offline-first): o Arquiteto propõe alternativa em ADR com prós/contras e custo.
- **Sempre A2:** qualquer custo novo (Supabase Pro, Vercel Pro, EAS pago, VPS), produção/publicação, e adotar fornecedor que recebe dados pessoais.
- Itens novos entram primeiro no catálogo como `em avaliação`; viram padrão só por revisão deste documento.

## 4. Exemplo: projeto novo
```
app-cliente/
├─ apps/web        # Next.js + Tailwind + shadcn/ui
├─ apps/mobile     # Expo (se houver app)
├─ supabase/       # migrations/, functions/, seed.sql (CLI do Supabase)
├─ packages/shared # tipos gerados + schemas Zod
└─ .github/workflows/ci.yml
```
Ambientes: dev local (`supabase start`), homologação (Vercel preview + projeto Supabase de teste) e produção (aprovada), como no [DevOps e SRE](../operacao/devops-sre.md).

## 5. Checklist do Arquiteto
- [ ] Partiu deste stack; cada desvio tem ADR com motivo.
- [ ] Nenhum item pago sem aprovação A2; limites do plano Free anotados no PRD.
- [ ] Região de dados definida (preferência `sa-east-1`, LGPD).
- [ ] RLS ligada em todas as tabelas; chaves secretas só no servidor.
- [ ] Repositório com regras do Cursor da VTX ([templates](../templates/cursor/README.md)).

## 6. Fontes
- Next.js: https://nextjs.org/docs
- Supabase: https://supabase.com/docs
- Expo: https://docs.expo.dev/
- shadcn/ui: https://ui.shadcn.com/docs
- Tailwind CSS: https://tailwindcss.com/docs
- Zod: https://zod.dev/
- Vercel AI SDK: https://ai-sdk.dev/docs
- Stripe Checkout: https://docs.stripe.com/payments/checkout
- ThoughtWorks Technology Radar (método de adoção por avaliação): https://www.thoughtworks.com/radar
