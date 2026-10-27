# Vercel
> Hospedagem e deploy · Status: **em avaliação** (adotada só para uso interno não comercial; uso comercial depende do Samuel) · Revisado em 2026-10-27 · VTX-099

## 1. O que é
Plataforma de hospedagem feita para Next.js: cada push gera um deploy, cada PR ganha uma URL de preview e as funções (rotas de API, Server Components) rodam sem servidor para administrar. É a hospedagem web padrão do [stack de referência](../../tecnologia/stack-de-referencia.md).

## 2. Quando usar / quando não usar
- **Usar:** apps Next.js com preview por PR; protótipos, PoCs e ferramentas internas da VTX que não geram receita.
- **Não usar no Hobby (grátis):** nada comercial. Pelas regras de uso justo da Vercel, comercial é qualquer deploy ligado a ganho financeiro de alguém envolvido, **inclusive o consultor pago que escreveu o código**. Portanto, site ou app de cliente e os sites comerciais da VTX, Tekto e med-hub no Vercel exigem o Pro.
- **Não usar para:** processo longo ou com estado (fila, worker) e site 100% estático simples, que fica melhor no GitHub Pages ou no Cloudflare Pages.

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Cloudflare Pages / Workers | site ou app comercial sem orçamento para o Pro | plano grátis sem a cláusula "não comercial" do Hobby (conferir ao adotar, VTX-104) |
| GitHub Pages | site estático, painel, documentação | grátis e já usado (painel-central) |
| VPS + Docker | backend longo, controle total | custo fixo e mais operação (A2) |

## 4. Custo e plano gratuito (conferido em 27/10/2026)
- **Hobby, grátis:** por mês, 100 GB de transferência, 1 milhão de requisições na CDN, 1 milhão de invocações de função, 4 h de CPU ativa e 5.000 transformações de imagem. Estourou o limite, o recurso **para por até 30 dias** (não cobra, mas o site cai).
- **Pro:** US$ 20/mês por assento de desenvolvedor (leitores grátis), com US$ 20 de crédito de uso incluído; proteção por senha custa mais US$ 20/mês por projeto.
- **Alerta A2:** criar time Pro, cartão, add-on ou qualquer uso comercial é **decisão do Samuel**. Até lá, a opção padrão para cliente é Cloudflare/GitHub Pages.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | homologação e produção | preview por PR + produção por tag (Pro se comercial) |
| [Site](../../processos/fluxos/site-landing-page.md) | publicação | só se precisar de Next.js dinâmico; estático vai para Pages |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | demo | Hobby, se não houver receita nem cliente pagante |
| [API](../../processos/fluxos/api-integracoes.md) / [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | deploy e rollback | Instant Rollback; logs da função na [observabilidade](../../operacao/observabilidade.md) |
| [Mobile](../../processos/fluxos/app-mobile.md) | — | não se aplica (app vai pelo EAS) |

## 6. Papel responsável
DevOps configura projeto, domínio e variáveis; Dev Frontend usa preview e logs; Arquiteto revisa região e limites; Samuel aprova plano pago e produção ([papéis](../../../agents/)).

## 7. Setup
1. Importar o repositório do GitHub (Vercel for GitHub): preview em todo PR, produção no branch/tag definido.
2. CLI local: `npx vercel link`, `npx vercel env pull .env.local`, `npx vercel --prebuilt` no CI se o build for no GitHub Actions ([CI/CD](../../engenharia/git-e-ci-cd.md)).
3. **Região:** as funções rodam por padrão em `iad1` (Washington). Com Supabase em São Paulo, fixar `"regions": ["gru1"]` no `vercel.json`.
4. MCP da Vercel (conectado em 23/10): usar para ler deploys e logs; mudança de produção só pelo Git.

## 8. Segredos e segurança/LGPD
- Chaves só nas variáveis do projeto, do tipo **Secret** (não legível depois de salva), separadas por ambiente (development, preview, production). Nunca no repositório nem no chat; `NEXT_PUBLIC_*` é público.
- Preview nunca usa dados reais nem chaves de produção. Ligar Vercel Authentication (proteção padrão dos previews).
- Dados pessoais de cliente na produção exigem conferir DPA e região (A2) e registrar no [desenvolvimento seguro](../../seguranca/desenvolvimento-seguro.md).
- Token de CI com escopo mínimo, guardado nos secrets do GitHub.

## 9. Checklist
- [ ] Projeto comercial? Se sim, Pro aprovado pelo Samuel ou outra hospedagem
- [ ] Região `gru1` fixada perto do banco
- [ ] Variáveis Secret por ambiente; nada sensível em `NEXT_PUBLIC_*`
- [ ] Preview protegido e sem dados reais
- [ ] Produção por tag e rollback testado
- [ ] Uso do mês acompanhado para não bater o limite do Hobby

## 10. Registro de adoção e Fontes
**ADR curto (27/10/2026):** *Contexto:* Next.js é o stack padrão e o Samuel conectou a Vercel. *Opções:* Vercel Hobby, Vercel Pro, Cloudflare, GitHub Pages. *Decisão:* Hobby só para uso interno não comercial; uso comercial aguarda decisão de custo do Samuel (A2). *Consequência:* clientes vão para Cloudflare/Pages até lá.
- Hobby Plan: https://vercel.com/docs/plans/hobby
- Fair Use Guidelines (uso comercial): https://vercel.com/docs/limits/fair-use-guidelines
- Preços: https://vercel.com/pricing
- Regiões: https://vercel.com/docs/regions
- Deployment Protection: https://vercel.com/docs/deployment-protection
- Variáveis de ambiente: https://vercel.com/docs/environment-variables
- CLI: https://vercel.com/docs/cli · GitHub: https://vercel.com/docs/git/vercel-for-github
