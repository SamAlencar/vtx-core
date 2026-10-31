# Cloudflare (DNS, Pages/Workers, Access, WAF)
> CI/CD e infraestrutura · Status: **recomendado** (DNS e proteção de todo domínio; hospedagem grátis alternativa à Vercel) · Revisado em 2026-10-31 · VTX-108

## 1. O que é
Rede de borda (CDN) com DNS gerenciado, proxy com WAF e anti-DDoS, hospedagem de sites e funções (Pages e Workers), controle de acesso a apps internos (Access, parte do Zero Trust), túnel sem porta aberta (`cloudflared`, Apache-2.0) e captcha sem fricção (Turnstile). A CLI `wrangler` é open source (Apache-2.0). Plano Free sem prazo; a Cloudflare o descreve como "para projetos pessoais ou não críticos", então cliente crítico avalia Pro (A2).

## 2. Quando usar / quando não usar
- **Usar:** DNS de todo domínio de cliente (grátis, rápido, com proxy); site estático e landing page; app comercial sem orçamento para Vercel Pro ([Vercel](../hospedagem/vercel.md) Hobby proíbe uso comercial); proteger painel interno ou homologação com Access; Turnstile em formulário ([site](../../processos/fluxos/site-landing-page.md)).
- **Não usar:** Next.js com recursos que só a Vercel suporta bem, sem testar o adaptador (OpenNext); processo longo ou com estado pesado (worker de fila, CPU alta); quando o cliente exige dados só no Brasil sem análise.

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Vercel Hobby/Pro | Next.js padrão | preview por PR nativo; Pro é A2 |
| GitHub Pages | site estático interno | já incluso no GitHub |
| VPS + [Docker](docker.md) + Caddy | backend longo | controle total, custo fixo (A2) |
| DNS do registrador | domínio sem site | sem proxy nem WAF |

## 4. Custo e plano gratuito (conferido em 31/10/2026)
- **DNS e proxy:** grátis, com anti-DDoS sem limite e SSL automático.
- **Pages Free:** 500 builds/mês, 1 build por vez, 20 min por build, 100 domínios por projeto, 20 mil arquivos (25 MiB cada). Funções contam na cota do Workers.
- **Workers Free:** 100 mil requisições/dia (zera à meia-noite UTC), 10 ms de CPU por requisição; ao estourar, erro 1027. Para projeto novo, a Cloudflare recomenda Workers com *static assets* em vez de Pages.
- **WAF Free:** Free Managed Ruleset (falhas graves e muito exploradas) e 5 regras customizadas; rate limiting básico. OWASP Core Ruleset e Managed Ruleset completo só no Pro (US$ 20/mês, A2).
- **Zero Trust/Access Free:** até 50 usuários, logs por 24 h; o 51º usuário é bloqueado (não há cobrança automática). O cadastro pede forma de pagamento mesmo no Free: A2 antes de ativar.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [Site](../../processos/fluxos/site-landing-page.md) | entrega | Pages/Workers + DNS + Turnstile |
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | produção | DNS, proxy e WAF na frente; Access na homologação |
| [API](../../processos/fluxos/api-integracoes.md) | produção | WAF e rate limit; Worker leve como gateway |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | demonstração | deploy grátis e Access para o cliente ver |

## 6. Papel responsável
DevOps/SRE gerencia DNS, regras e deploy; Segurança revisa WAF e Access; Devs mantêm `wrangler.toml`; Samuel aprova plano pago, cadastro com cartão e transferência de domínio de cliente ([papéis](../../../agents/)).

## 7. Setup
1. Conta do projeto (e-mail VTX ou do cliente, nunca pessoal); domínio do cliente adicionado com os nameservers da Cloudflare; 2FA ligado.
2. DNS como código: exportar a zona (BIND) no repo ou usar OpenTofu com o provider da Cloudflare; mudança por PR.
3. SSL/TLS "Full (strict)", HSTS depois de validado, "Always Use HTTPS".
4. Site: `npx wrangler deploy` (Workers + assets) ou Pages ligado ao GitHub; preview por branch; deploy pelo [GitHub Actions](github-actions.md) com token de escopo mínimo.
5. WAF: Free Managed Ruleset ligado; regras customizadas para `/admin` e bloqueio por país só se o PRD pedir; rate limit no login.
6. Homologação: aplicação no Access com login por e-mail (OTP) só para a equipe e o cliente.

## 8. Segredos e segurança/LGPD
- API token por projeto, só com as permissões necessárias (ex.: "Edit Workers", "DNS Edit" da zona), em segredo do GitHub; nunca a Global API Key.
- Segredos do Worker via `wrangler secret`, fora do repo.
- Proxy vê todo o tráfego (TLS termina na borda): constar como suboperador na política de privacidade; logs do Free ficam 24 h.
- `cloudflared` evita abrir porta no servidor do cliente ([desenvolvimento seguro](../../seguranca/desenvolvimento-seguro.md)).

## 9. Checklist
- [ ] Conta do projeto com 2FA; domínio com DNS na Cloudflare
- [ ] Zona exportada/versionada no repo
- [ ] TLS Full (strict) e HTTPS forçado
- [ ] Free Managed Ruleset ligado e rate limit no login
- [ ] Homologação atrás do Access
- [ ] Token de API com escopo mínimo no CI
- [ ] Cotas (builds, requisições/dia) acompanhadas; plano pago só com A2

## 10. Registro de avaliação e Fontes
**ADR curto (31/10/2026):** *Contexto:* Vercel Hobby não serve para uso comercial e todo domínio precisa de DNS e proteção. *Opções:* Cloudflare Free, DNS do registrador, Vercel Pro. *Decisão:* Cloudflare para DNS/WAF de todos os domínios e como hospedagem grátis padrão de site comercial; Vercel segue padrão para Next.js interno. *Consequência:* testar o adaptador OpenNext antes de levar Next.js para Workers.
- Planos: https://www.cloudflare.com/plans/
- Limites do Pages: https://developers.cloudflare.com/pages/platform/limits/
- Limites do Workers: https://developers.cloudflare.com/workers/platform/limits/
- Pages para Workers: https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/
- Regras customizadas do WAF: https://developers.cloudflare.com/waf/custom-rules/
- Managed rules: https://developers.cloudflare.com/waf/managed-rules/
- Zero Trust (preços): https://www.cloudflare.com/plans/zero-trust-services/
- Assentos do Zero Trust: https://developers.cloudflare.com/cloudflare-one/faq/getting-started-faq/
- cloudflared: https://github.com/cloudflare/cloudflared
