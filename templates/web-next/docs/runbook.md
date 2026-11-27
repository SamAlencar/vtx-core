# Runbook — __NOME_DO_PROJETO__

Operação, preview e resposta a incidente (DevOps/SRE).
SLA técnico e canal de suporte: [suporte-e-sla.md](../../../knowledge/operacao/suporte-e-sla.md) (VTX-199).

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

## Saúde, monitor e logs

- **Health:** `GET /api/health` (ou `/` se ainda não houver rota de health) deve responder **200** sem autenticação. Neste template a rota `/api/health` ainda não existe; o monitor usa `/` até ela ser criada.
- **Monitor gratuito:** UptimeRobot ou Better Stack Uptime (tier free), intervalo 5 min, alerta para o e-mail do canal de suporte abaixo. Registrar aqui a URL do monitor após o go-live.
- **URL do monitor:** _preencher no go-live_
- Logs do preview Cloudflare: painel Pages/Workers (retenção curta no Free).

## Canal de suporte

- **Entrada:** e-mail `suporte+__NOME_DO_PROJETO__@…` *ou* formulário do projeto (um canal só).
- **Triagem:** agente classifica Sev e tipo; 1ª resposta no prazo do [SLA](../../../knowledge/operacao/suporte-e-sla.md).
- **Nível de SLA deste projeto:** Essencial (4 h/mês) / Evolução (12 h/mês) — _marcar um_.

## Rollback

Republicar o deploy anterior no painel da Cloudflare (ou o commit anterior no branch de produção).

## Incidentes

| Sev | Ação imediata | A2? |
|---|---|---|
| SEV1 | Rollback ou desligar flag; avisar Samuel em seguida | Depois do mitigar, se envolver dados/cobrança/cliente |
| SEV2 | Corrigir ou workaround; registrar no ticket | Comunicação externa e gasto |
| SEV3 | Backlog ou resposta no canal | — |

SEV1 e SEV2 geram postmortem curto em `docs/postmortems/` neste repositório (modelo em [suporte-e-sla.md](../../../knowledge/operacao/suporte-e-sla.md)). Apagar dados, cobrança, falar com o cliente ou plano pago continuam A2.
