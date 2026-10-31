# Sentry
> Observabilidade · Status: **recomendado** (SaaS Developer em projetos pequenos; GlitchTip se precisar de mais) · Revisado em 2026-10-31 · VTX-107

## 1. O que é
Serviço de rastreamento de erros e desempenho: agrupa exceções com stack trace, release e usuário afetado, além de tracing, logs, session replay, cron e uptime. SDKs (JavaScript, Python, React Native etc.) são MIT; o servidor é *Fair Source* (FSL 1.1, vira Apache-2.0 após 2 anos) e pode ser self-hosted. Complementa a [observabilidade](../../operacao/observabilidade.md) (VTX-022), que define logs JSON e `trace_id`.

## 2. Quando usar / quando não usar
- **Usar:** produção de qualquer SaaS, API ou app mobile, para saber do erro antes do cliente; source maps e releases ligados ao deploy.
- **Não usar:** como único log (não substitui logs da hospedagem); para dados sensíveis em payload; quando o volume passar da cota grátis sem aprovação de plano.

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Sentry SaaS Developer | padrão em projeto pequeno | zero infra, US$ 0 |
| GlitchTip (MIT) | cota estourou, dados no Brasil, vários usuários | compatível com SDK do Sentry, leve, self-host |
| Sentry self-host | raramente | 4 CPU, 16 GB RAM + 16 GB swap; manutenção alta |
| Crashlytics | só crashes mobile | grátis ([Firebase](../backend/firebase.md)) |

## 4. Custo e plano gratuito (conferido em 31/10/2026)
- **Developer, US$ 0:** 1 usuário, 5 mil erros/mês, 5M spans, 5 GB de logs, 50 replays, 1 cron e 1 uptime monitor, 1 GB de anexos, alertas por e-mail, MCP. Ao estourar, eventos são descartados até o próximo ciclo.
- **Team US$ 26/mês** (anual; usuários ilimitados, 50 mil erros, integrações) e **Business US$ 80/mês:** pagos, A2 (Samuel). Preferir GlitchTip self-host antes de pagar.
- Self-host do Sentry é grátis, mas custa máquina grande.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | produção | SDK Next.js, source maps, releases |
| [Mobile](../../processos/fluxos/app-mobile.md) | produção | SDK React Native/Expo |
| [API](../../processos/fluxos/api-integracoes.md) | produção | SDK do backend + `trace_id` |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | triagem | issues viram tarefas com prioridade |

## 6. Papel responsável
DevOps/SRE cria projetos, DSN e alertas; Devs instrumentam e corrigem; QA confere o filtro de dados pessoais; Samuel aprova plano pago ([papéis](../../../agents/)).

## 7. Setup
1. Um projeto por app e ambiente (`environment: dev/prod`); DSN em variável de ambiente.
2. `npx @sentry/wizard` no projeto (Next.js/React Native) ou SDK manual; `release` = SHA do commit, enviado pelo CI com source maps (token de auth como segredo).
3. Amostragem: `tracesSampleRate` baixo (ex.: 0,1) para caber na cota; replay só em erro.
4. Alertas por e-mail para erro novo e pico; regra de *inbound filter* para ruído (bots, extensões).
5. GlitchTip: mesmo SDK, trocando só o DSN.

## 8. Segredos e segurança/LGPD
- DSN não é segredo forte (vai no front), mas o token de auth do CI é.
- `sendDefaultPii: false`; `beforeSend` removendo CPF, e-mail, tokens e corpo de requisição; scrubbing do servidor ligado.
- Dados do SaaS ficam nos EUA ou UE (sem região Brasil): transferência internacional na política de privacidade; se o cliente exigir dado no Brasil, GlitchTip self-host ([desenvolvimento seguro](../../seguranca/desenvolvimento-seguro.md)).

## 9. Checklist
- [ ] Projeto por app e ambiente; DSN em variável
- [ ] Release + source maps pelo CI
- [ ] PII filtrada (`sendDefaultPii: false`, `beforeSend`) e testada
- [ ] Amostragem dentro da cota grátis
- [ ] Alerta de erro novo chegando
- [ ] Plano pago só com A2; GlitchTip avaliado antes

## 10. Registro de avaliação e Fontes
**ADR curto (31/10/2026):** *Contexto:* VTX-022 deixou Sentry para avaliar. *Opções:* Sentry SaaS, Sentry self-host, GlitchTip. *Decisão:* Sentry Developer em projetos pequenos; GlitchTip self-host quando faltar cota, usuário ou residência de dados. *Consequência:* mesmo SDK nos dois, troca só o DSN.
- Preços: https://sentry.io/pricing/
- Mudança de cotas do Developer: https://www.sentry.help/en/articles/13965033-how-is-my-plan-changing-august-27-2025
- Self-host (requisitos, FSL): https://develop.sentry.dev/self-hosted/
- Dados sensíveis: https://docs.sentry.io/platforms/javascript/data-management/sensitive-data/
- Next.js: https://docs.sentry.io/platforms/javascript/guides/nextjs/
- React Native: https://docs.sentry.io/platforms/react-native/
- Residência de dados: https://docs.sentry.io/organization/data-storage-location/
- GlitchTip: https://glitchtip.com/
