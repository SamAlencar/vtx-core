# Fluxo de projeto: site / landing page

> VTX-070 · Fase F1 · Base de Conhecimento. Especializa o [SOP entre agentes](../fluxo-entre-agentes.md) para sites institucionais e páginas de conversão. Vale quando a [triagem](triagem.md) define `tipo_principal: site-landing-page`, ou como módulo de conteúdo de outro fluxo.

## 1. Conceitos
- **Site institucional:** conjunto de páginas de divulgação (empresa, serviços, blog, contato). Conteúdo e SEO pesam mais que regras de negócio.
- **Landing page:** página única (ou poucas) com um objetivo de conversão: lead, demo, inscrição ou venda. Mensagem, prova social e formulário curtos.
- **Conteúdo primeiro:** textos, imagens e estrutura de URLs são artefatos de Produto/UX antes do código. CMS headless ou Markdown/docs-as-code quando o cliente atualiza sozinho.
- **Performance e SEO:** Core Web Vitals (LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 no percentil 75) e HTML semântico indexável. Formulário simples; lógica de lead ou CRM entra como módulo [API e integrações](api-integracoes.md).

## 2. Etapas do fluxo

| # | Etapa | Papéis | Artefatos | Portão |
|---|---|---|---|---|
| 0 | Triagem | Orquestrador | `projects/<p>/ficha.yaml` | `tipo_principal: site-landing-page` |
| 1 | Descoberta | Produto (+ UX) | Objetivo de conversão, público, mapa de páginas/seções, requisitos de SEO e formulários | **Samuel aprova escopo e mensagem** |
| 2 | Conteúdo e UX | Produto + UX/UI | Copy, wireframes/protótipo, guia visual mínimo (WCAG 2.2 AA), lista de assets | Produto valida contra o objetivo |
| 3 | Arquitetura | Arquiteto | ADR de stack (estático, SSG, CMS), hospedagem, domínio/DNS, formulário/CRM | Revisão do Orquestrador; Segurança se houver dado pessoal no formulário |
| 4 | Fundação | DevOps + Dev Frontend | Repositório, CI (lint, build, Lighthouse CI), preview por PR, analytics e consentimento | Preview público funcionando |
| 5 | Incrementos | Dev Frontend + QA | Página/seção por PR; formulário com validação e spam-protection | CI verde, aceite, revisão independente |
| 6 | Endurecimento | QA + Segurança | Lighthouse (Performance/Acessibilidade/SEO ≥ 90), WCAG 2.2 AA, links quebrados, LGPD do formulário | Sem falha crítica ou alta aberta |
| 7 | Lançamento | DevOps + Orquestrador | DNS/HTTPS, sitemap/robots, Search Console, redirecionamentos | **Samuel aprova publicação** |
| 8 | Operação e evolução | DevOps + Produto | Monitoramento de Core Web Vitals e conversão; demandas novas em [manutenção](manutencao-evolucao.md) | Retrospectiva registrada |

As etapas 5 e 6 repetem por página ou seção. Cada incremento termina em preview para o Samuel ver.

## 3. Pontos de aprovação do Samuel
1. Escopo, objetivo de conversão e tom da mensagem (etapa 1).
2. Domínio, hospedagem paga e ferramentas de analytics/CRM (etapa 3).
3. Coleta de dados pessoais no formulário (base legal, aviso de privacidade), na etapa 3, com Segurança.
4. Publicação em produção e mudanças que alterem a URL canônica ou redirecionamentos críticos (etapa 7).

## 4. Itens específicos de site e landing
- **Stack típica:** site estático ou SSG (HTML/CSS, Astro, Next estático, Hugo) em Pages/Netlify/Vercel; CMS headless só se o cliente edita com frequência. Evitar SPA pura se SEO for requisito.
- **SEO técnico:** título e meta description únicos, headings hierárquicos, `canonical`, Open Graph, sitemap.xml, robots.txt, dados estruturados básicos (Organization/WebSite) quando couber.
- **Formulário:** campos mínimos, validação no cliente e no servidor/serverless, proteção anti-spam (honeypot ou Turnstile/hCaptcha), confirmação ao usuário e registro no CRM/e-mail. Sem armazenar dado sensível sem necessidade.
- **Imagens e fontes:** formatos modernos (WebP/AVIF), dimensões explícitas (reduz CLS), lazy-load abaixo da dobra, fontes com `font-display: swap`.
- **Acessibilidade e privacidade:** contraste e teclado (WCAG 2.2 AA); banner/consentimento de cookies se houver analytics não essencial; política de privacidade linkada no formulário.
- **Analytics:** evento de conversão definido na etapa 1 (ex.: envio do formulário); medir no lançamento, não só pageviews.

## 5. Riscos típicos e mitigação

| Risco | Mitigação |
|---|---|
| Conteúdo atrasa o lançamento | Bloquear etapa 4 até copy e assets da home/landing estarem prontos |
| LCP ruim (hero pesado) | Imagem otimizada, prioridade no LCP, CSS crítico mínimo |
| Formulário gera spam ou lead perdido | Anti-spam, log de falhas, teste ponta a ponta até o CRM |
| SEO quebrado após redesign | Checklist de redirects 301, Search Console pós-go-live |
| Dependência de tema/CMS opaco | ADR prefere código versionado; tema só com escape hatch |
| Violação de LGPD no lead | Aviso + base legal, retenção curta, sem lista de e-mail sem opt-in |

## 6. Exemplo
"Landing para captar demos de um produto B2B." Etapa 1: conversão = agendar demo; Samuel aprova a mensagem. Etapa 3: ADR-001 Astro estático + formulário serverless para o CRM; domínio já existe. Etapa 4: preview por PR e Lighthouse CI. Etapa 5: seções hero, prova social, FAQ e formulário. Etapa 6: CLS alto por fonte sem reserva — corrigido com `size-adjust`. Etapa 7: Samuel aprova; DNS e Search Console no ar; evento de conversão validado.

## 7. Checklist de conclusão
- [ ] Objetivo de conversão, mapa de páginas e mensagem aprovados pelo Samuel
- [ ] Copy, assets e protótipo das seções principais prontos
- [ ] ADR de stack, hospedagem, domínio e formulário/CRM salvos
- [ ] Preview por PR; Lighthouse Performance/Acessibilidade/SEO ≥ 90
- [ ] Core Web Vitals no alvo (LCP/INP/CLS); WCAG 2.2 AA nas páginas principais
- [ ] Formulário testado ponta a ponta; anti-spam e aviso de privacidade
- [ ] Sitemap, robots, HTTPS e Search Console; publicação aprovada pelo Samuel
- [ ] Analytics de conversão e retrospectiva registrados

## Fontes
- Google, *Core Web Vitals* (LCP, INP, CLS): https://web.dev/articles/vitals · *Understanding Core Web Vitals and Google Search*: https://developers.google.com/search/docs/appearance/core-web-vitals
- Google Search Central, *SEO Starter Guide*: https://developers.google.com/search/docs/fundamentals/seo-starter-guide · *Sitemaps*: https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
- W3C, *WCAG 2.2*: https://www.w3.org/TR/WCAG22/ · MDN, *HTML: A good basis for accessibility*: https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML
- web.dev, *Optimize LCP*: https://web.dev/articles/optimize-lcp · *Optimize CLS*: https://web.dev/articles/cls · *Optimize INP*: https://web.dev/articles/optimize-inp
- Schema.org, *Organization* / *WebSite*: https://schema.org/ · Open Graph Protocol: https://ogp.me/
- Cloudflare, *Turnstile*: https://developers.cloudflare.com/turnstile/ · OWASP, *Cheat Sheet Series — Input Validation*: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- Brasil, Lei nº 13.709/2018 (LGPD): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
