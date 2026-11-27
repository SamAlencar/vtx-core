# Observabilidade (logs, métricas, traces)

> VTX-022 · Fase F3 · Base de Conhecimento. Como o **DevOps/SRE** ([devops-sre.md](../../agents/devops-sre.md)) e os **Devs** tornam o sistema explicável em produção. Continua [DevOps e SRE](devops-sre.md) (SLOs, incidentes) e respeita [segurança](../seguranca/desenvolvimento-seguro.md) (log sem PII). Ferramentas seguem o [stack de referência](../tecnologia/stack-de-referencia.md).

## 1. Conceitos
- **Observabilidade:** responder "o que está acontecendo e por quê?" só com os sinais que o sistema emite, sem novo deploy.
- **Três sinais:** **logs** (evento com contexto, JSON), **métricas** (números agregados no tempo: taxa, erro, latência) e **traces** (o caminho de uma requisição entre serviços, em *spans*). O `trace_id` liga os três.
- **Golden signals / RED:** latência, tráfego, erros e saturação (Google SRE); para APIs, *Rate, Errors, Duration*.
- **OpenTelemetry (OTel):** padrão aberto da CNCF para instrumentar uma vez e mandar a qualquer backend. É o padrão VTX: evita prender o código a fornecedor.
- **Alerta por *burn rate*:** alerta quando o *error budget* do SLO está sendo gasto rápido demais, não quando uma métrica qualquer oscila.

## 2. Padrão VTX por sinal
| Sinal | Como emitir | Onde ver (grátis) |
|---|---|---|
| Logs | JSON estruturado (`pino` no Node; `console.log` de objeto em Edge/Vercel), campos fixos: `ts`, `level`, `msg`, `service`, `env`, `trace_id`, `request_id`, `user_ref` (id opaco) | Logs da Vercel e do Supabase (painel e CLI); retenção curta, exportar só se necessário |
| Métricas | Derivadas dos logs e dos painéis nativos (Vercel Analytics/Speed Insights do plano Hobby, relatórios do Supabase); contadores de negócio como eventos de log | Painéis nativos; Prometheus + Grafana OSS só com VPS |
| Traces | `@vercel/otel` / SDK OTel em Next.js (`instrumentation.ts`), propagando `traceparent` (W3C) | Exportador OTLP para Grafana Tempo ou Jaeger self-host; sem backend, só `trace_id` nos logs |
| Erros | `try/catch` na borda + `error.tsx`/handler global com log `level=error` e `trace_id` | Logs; GlitchTip (open source, compatível com SDK do Sentry) se self-host; [Sentry](../ferramentas/observabilidade/sentry.md) Developer (grátis) em projeto pequeno |

**Níveis:** `error` (ação humana ou alerta), `warn` (degradação tolerada), `info` (evento de negócio/requisição), `debug` (só dev/homologação). Produção roda em `info`.

**LGPD e segredos:** nunca logar senha, token, chave, CPF, e-mail, telefone, endereço, dado de saúde ou corpo de requisição inteiro. Use `user_ref` opaco e a opção `redact` do pino (`req.headers.authorization`, `*.password`, `*.cpf`). Prompts e respostas de LLM só em homologação, anonimizados.

## 3. Alertas e painéis
- **Um painel por serviço** com RED + saturação (cota do Supabase/Vercel) e o SLO corrente.
- **Alertas só sobre SLO** ([SLOs padrão](devops-sre.md)): *burn rate* rápido (2 % do budget em 1 h) → SEV2; lento (10 % em 3 dias) → issue. Além disso: job agendado que falhou, cota > 80 %, certificado vencendo.
- **Todo alerta tem dono e link de runbook**; alerta ignorado 3 vezes é corrigido ou apagado.
- **Canal:** e-mail/GitHub Issue do projeto; SEV1/2 seguem a escada de incidentes do [devops-sre.md](devops-sre.md).
- **Monitor externo grátis:** verificação HTTP agendada pelo GitHub Actions (`curl -f` no `/api/health` a cada 15 min, abre issue se falhar) antes de qualquer serviço pago.

## 4. Metodologia (por projeto)
1. No PRD: SLIs/SLOs e eventos de negócio que importam (ex.: "pedido criado").
2. Na arquitetura: onde nasce e como propaga o `trace_id` (borda → API → banco/funções).
3. No código: logger único (`lib/logger.ts`), *middleware* que gera `request_id`, `instrumentation.ts` do OTel; teste unitário de que a redação de PII funciona.
4. No CI: lint impede `console.log` solto fora do logger (exceto scripts).
5. Antes de produção: painel e alertas criados, runbook "onde ver logs" preenchido, simulação de um erro conferida de ponta a ponta.
6. Mensal: revisar alertas ruidosos, custo/retenção e SLOs.

## 5. Exemplo (Next.js + Supabase)
```ts
// lib/logger.ts
import pino from "pino";
export const logger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  base: { service: "app-web", env: process.env.VERCEL_ENV },
  redact: ["req.headers.authorization", "*.password", "*.cpf", "*.email"],
});
// uso: logger.info({ trace_id, user_ref, pedido_id }, "pedido criado");
```
```ts
// instrumentation.ts
import { registerOTel } from "@vercel/otel";
export function register() { registerOTel({ serviceName: "app-web" }); }
```

## 5b. Execução de agente: log e custo (VTX-179)
Cada execução de agente grava **uma linha JSON** com run_id, trace_id, cliente, agente, modelo, tokens_entrada, tokens_saida, custo_usd, duracao_ms, status, erro e ts (UTC). A implementação de referência é [core/agente/telemetria.py](../../core/agente/telemetria.py) e usa só a biblioteca padrão:
- `redigir()` troca e-mail, tokens (`sk-`, `ghp_`, JWT, `Bearer`), CPF e CNPJ com máscara, CNPJ de 14 dígitos e telefone com máscara por marcadores. Vale para a mensagem de erro e outros campos livres. **Não** redige `cliente`, `agente`, `run_id` nem `trace_id` (um cliente que é um e-mail precisa continuar batendo com o orçamento). Fica de fora, de propósito: CPF e telefone com 11 dígitos sem máscara (um celular como `11987654321` não deve virar `[CPF]`).
- `custo_usd()` calcula o custo pelo preço por milhão de tokens. `custo_por_cliente_dia()` soma por cliente e dia, em UTC. Linhas JSON corrompidas são ignoradas e contadas em `ler_detalhado()`.
- `Telemetria.execucao()` aplica um **limite brando**: o orçamento diário do cliente é conferido só na entrada. Se já estiver esgotado, levanta `OrcamentoExcedido` e nada roda. Uma execução já iniciada pode passar do limite, e execuções paralelas podem ler o mesmo gasto e passar juntas. `gasto_hoje()` relê o arquivo inteiro a cada conferência; em produção isso pede rotação por dia ou um agregado. A linha é gravada mesmo quando a execução falha (inclusive `BaseException`, repropagada).
- O caminho de referência é `logs/agentes.jsonl`. A pasta `logs/` está no `.gitignore` do vtx-core: log com dado de cliente não entra no repositório.
```python
t = Telemetria(Path("logs/agentes.jsonl"), orcamento_dia={"cliente-a": 2.0})
with t.execucao("cliente-a", "dev", "modelo-x", trace_id=trace_id) as ex:
    resp = chamar_modelo(...)
    ex.somar(resp.in_tok, resp.out_tok, custo_usd(resp.in_tok, resp.out_tok, 3.0, 15.0))
```
Os testes estão em `tests/test_telemetria.py` e cobrem os campos, a PII, a soma, o orçamento, cliente-e-mail, linha corrompida e interrupção. Franquia por cliente e BYOK ficam na VTX-149.

## 6. Checklist
- [ ] Logs em JSON com `service`, `env`, `trace_id`, `request_id`; nível `info` em produção.
- [ ] Redação de PII/segredos configurada e testada.
- [ ] Agentes: uma linha JSON por execução com custo e orçamento diário por cliente (§5b).
- [ ] OTel instrumentado (`instrumentation.ts`) e `traceparent` propagado.
- [ ] Painel RED + saturação por serviço; SLO visível.
- [ ] Alertas por *burn rate* com dono e runbook; health check agendado.
- [ ] Nenhuma ferramenta paga; self-host só com aprovação de custo (A2) se exigir VPS.

## 7. Fontes
- Google SRE Book, cap. 6 "Monitoring Distributed Systems": https://sre.google/sre-book/monitoring-distributed-systems/
- Google SRE Workbook, "Alerting on SLOs": https://sre.google/workbook/alerting-on-slos/
- OpenTelemetry, documentação: https://opentelemetry.io/docs/
- Next.js, OpenTelemetry: https://nextjs.org/docs/app/guides/open-telemetry
- Vercel, Runtime Logs: https://vercel.com/docs/logs/runtime
- Supabase, Logging: https://supabase.com/docs/guides/telemetry/logs
- pino, redação: https://getpino.io/#/docs/redaction
- GlitchTip (open source): https://glitchtip.com/
