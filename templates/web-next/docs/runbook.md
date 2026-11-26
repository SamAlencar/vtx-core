# Runbook — __NOME_DO_PROJETO__

Operação, preview e resposta a incidente (DevOps/SRE).

## Preview em hospedagem gratuita com uso comercial permitido

O padrão para site ou app de cliente é **Cloudflare Pages** (plano Free). A Cloudflare não tem a cláusula "não comercial" do Vercel Hobby. Limites do Free (conferidos na base VTX em 31/10/2026): 500 builds/mês, 1 build por vez, 20 min por build. Cliente crítico avalia o Pro (A2).

Como publicar um preview:

1. Repositório no GitHub do cliente (não no vtx-core).
2. No painel da Cloudflare: Workers & Pages → criar projeto a partir do repositório.
3. Build: `npm ci && npm run build`. Diretório de saída: `.next` se usar o adaptador OpenNext / `@cloudflare/next-on-pages`; siga o guia atual do adaptador no primeiro deploy (A1, registrar no ADR).
4. Variáveis de ambiente (URL e chave anônima do Supabase) só no painel, nunca no git.
5. Publicar produção é A2.

**Vercel:** o stack Next.js roda bem lá, mas o plano Hobby é só para uso interno não comercial. Site de cliente ou qualquer uso ligado a receita exige Vercel Pro, que é A2. Até essa aprovação, não use Vercel para este projeto.

GitHub Pages serve página estática; este template é Next.js, então não é o padrão.

## Saúde e logs

No preview da Cloudflare: logs do Pages/Workers no painel (retenção curta no Free).

## Rollback

Republicar o deploy anterior no painel da Cloudflare (ou o commit anterior no branch de produção).

## Incidentes

Quem avisar, o que registrar, o que é A2 (apagar dados, cobrança, falar com o cliente, plano pago).
