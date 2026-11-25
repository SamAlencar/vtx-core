# Fluxo de projeto: API e integrações

> VTX-069 · Fase F1 · Base de Conhecimento. Especializa o [SOP entre agentes](../fluxo-entre-agentes.md) para entregas sem tela própria: APIs, webhooks e integrações entre sistemas (ERP, pagamento, marketplace). Vale quando a [triagem](triagem.md) define `tipo_principal: api-integracoes`, ou como módulo de outro fluxo.

## 1. Conceitos
- **API própria vs. integração:** a API própria expõe dados ou regras da VTX para outros consumirem; a integração conecta sistemas de terceiros (ex.: ERP → Mercado Livre). Muitas entregas têm as duas.
- **Contrato primeiro:** o contrato é o primeiro artefato e a fonte da verdade. **OpenAPI** para HTTP síncrono; **AsyncAPI** para eventos e filas. Código, mocks, testes e documentação saem dele.
- **Estilos:** síncrono (REST/HTTP, resposta na hora), assíncrono (webhook, fila, evento) e lote (arquivo ou carga agendada). A escolha é ADR e depende de volume, latência e de quem inicia a troca.
- **Idempotência:** repetir a mesma chamada não duplica o efeito. GET, PUT e DELETE já são idempotentes (RFC 9110); POST com efeito usa chave `Idempotency-Key`. É o que permite retentativa segura.
- **Camada anticorrupção:** um adaptador traduz o modelo do terceiro para o nosso, para que mudanças do parceiro não se espalhem pelo código.
- **Ferramentas:** padrão — GitHub Actions, Cursor, Cloudflare, Supabase, Stripe, Sentry, Docker. Opcional — Vercel, Appwrite. Detalhe na [matriz ferramenta × fluxo](../../ferramentas/README.md#matriz); a escolha formal fica no [stack de referência](../../tecnologia/stack-de-referencia.md) e no ADR.

## 2. Etapas do fluxo

| # | Etapa | Papéis | Artefatos | Portão |
|---|---|---|---|---|
| 0 | Triagem | Orquestrador | `projects/<p>/ficha.yaml` | `tipo_principal: api-integracoes` |
| 1 | Descoberta | Produto (+ Arquiteto) | Sistemas envolvidos, donos, volume, SLA, dados trafegados, credenciais e sandbox disponíveis | **Samuel aprova escopo e parceiros** |
| 2 | Contrato e arquitetura | Arquiteto (+ Segurança) | OpenAPI/AsyncAPI, mapeamento de campos (de/para), ADRs: estilo, autenticação, retentativa, versionamento | Revisão do Orquestrador; Segurança obrigatória |
| 3 | Fundação | DevOps + Dev Backend | CI com validação do contrato (lint), mock gerado, segredos no cofre, ambientes com sandbox do parceiro, logs com ID de correlação | Mock e sandbox respondendo |
| 4 | Incrementos | Dev Backend + QA | Um fluxo de dados por PR (ex.: "pedido criado"), testes de contrato e de erro | CI verde, aceite, revisão independente |
| 5 | Endurecimento | QA + Segurança + DevOps | OWASP API Top 10, limites de taxa, teste de falha do parceiro (timeout, 5xx, duplicata), reprocessamento | Sem falha crítica ou alta aberta |
| 6 | Lançamento | DevOps + Orquestrador | Credenciais de produção, runbook, alertas, documentação para consumidores | **Samuel aprova produção** |
| 7 | Operação e evolução | DevOps/SRE + Produto | Painel de erros e filas, depreciação de versões; demandas novas em [manutenção](manutencao-evolucao.md) | Retrospectiva registrada |

As etapas 4 e 5 repetem por fluxo de dados. Nada vai para produção sem ter rodado contra o sandbox do parceiro.

## 3. Pontos de aprovação do Samuel
1. Escopo, parceiros e quais dados trafegam (etapa 1).
2. Custos recorrentes: planos de API pagos, gateway, fila ou iPaaS (etapa 2).
3. Dados pessoais ou financeiros entre empresas (LGPD, base legal e contrato com o parceiro), na etapa 2, com Segurança.
4. Ativação em produção e qualquer mudança que quebre consumidores (versão nova obrigatória), nas etapas 6 e 7.

## 4. Itens específicos de API e integração
- **Erros:** formato único *Problem Details* (RFC 9457), com `type`, `title`, `status` e `detail`; nunca expor pilha ou segredo.
- **Retentativa e falhas:** retentar só erros transitórios (timeout, 429, 5xx), com espera exponencial e *jitter*; *circuit breaker* para parceiro fora do ar; mensagem que falha de vez vai para fila de mortas (DLQ) com reprocessamento manual.
- **Webhooks:** validar assinatura HMAC e carimbo de tempo, responder 2xx rápido e processar em fila, tratar entrega repetida e fora de ordem (guardar ID do evento).
- **Autenticação:** OAuth 2.0 *client credentials* entre sistemas, seguindo a RFC 9700; chave de API só quando o parceiro exigir. Escopo mínimo, rotação e segredos só no cofre ou CI.
- **Versionamento:** SemVer no contrato; mudança incompatível = versão nova (`/v2`). Anunciar a saída da antiga com os cabeçalhos `Deprecation` (RFC 9745) e `Sunset` (RFC 8594).
- **Observabilidade:** ID de correlação de ponta a ponta, métricas por parceiro (latência, taxa de erro, fila) e alerta quando a DLQ cresce.

## 5. Riscos típicos e mitigação

| Risco | Mitigação |
|---|---|
| Parceiro muda a API sem aviso | Camada anticorrupção, teste de contrato diário contra o sandbox, alerta de schema |
| Duplicidade (pedido ou cobrança em dobro) | Idempotency-Key, ID de evento guardado, teste de reenvio |
| Parceiro lento ou fora do ar | Timeout curto, retentativa com limite, circuit breaker, fila |
| Sandbox diferente da produção | Lista de diferenças conhecidas; primeira carga em produção acompanhada |
| Vazamento de credencial | Cofre/CI, escopo mínimo, rotação, varredura de segredos no CI |
| Limite de taxa estourado | Respeitar 429 e `Retry-After`, fila com vazão controlada |

## 6. Exemplo
"ERP do cliente precisa enviar pedidos ao Mercado Livre e receber o status." Etapa 1: dois fluxos (pedido de saída, status de volta); Samuel aprova o parceiro e os dados do comprador. Etapa 2: AsyncAPI para eventos do ERP, OpenAPI do adaptador; ADR-001 fila + webhook; de/para de campos. Etapa 3: mock e sandbox do marketplace no CI. Etapa 4: incremento 1 "pedido criado", incremento 2 "status atualizado". Etapa 5: teste de reenvio acha pedido duplicado; corrigido com chave de idempotência. Etapa 6: Samuel aprova a ativação; primeira carga acompanhada pelo DevOps.

## 7. Checklist de conclusão
- [ ] Escopo, parceiros e dados aprovados pelo Samuel
- [ ] Contrato OpenAPI/AsyncAPI e de/para salvos e validados no CI
- [ ] ADRs de estilo, autenticação, retentativa e versionamento
- [ ] Idempotência e tratamento de duplicata testados
- [ ] Webhooks com assinatura validada e processamento em fila
- [ ] Erros em Problem Details; retentativa, circuit breaker e DLQ funcionando
- [ ] OWASP API Top 10 verificado; segredos só no cofre/CI
- [ ] Testado no sandbox; produção aprovada pelo Samuel
- [ ] Runbook, alertas, documentação para consumidores e retrospectiva registrados

## Fontes
- OpenAPI Initiative, *OpenAPI Specification*: https://spec.openapis.org/oas/latest.html · AsyncAPI, *Specification*: https://www.asyncapi.com/docs/reference/specification/latest
- IETF, RFC 9110 *HTTP Semantics*: https://www.rfc-editor.org/rfc/rfc9110 · RFC 9457 *Problem Details for HTTP APIs*: https://www.rfc-editor.org/rfc/rfc9457 · *The Idempotency-Key HTTP Header Field* (rascunho): https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
- IETF, RFC 9700 *Best Current Practice for OAuth 2.0 Security*: https://www.rfc-editor.org/rfc/rfc9700 · RFC 9745 *Deprecation*: https://www.rfc-editor.org/rfc/rfc9745 · RFC 8594 *Sunset*: https://www.rfc-editor.org/rfc/rfc8594
- OWASP, *API Security Top 10 (2023)*: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- Microsoft, padrões *Retry*: https://learn.microsoft.com/en-us/azure/architecture/patterns/retry · *Circuit Breaker*: https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker · *Anti-corruption Layer*: https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer
- Hohpe e Woolf, *Enterprise Integration Patterns*: https://www.enterpriseintegrationpatterns.com/ · Pact, *Contract testing*: https://docs.pact.io/
- Standard Webhooks: https://www.standardwebhooks.com/ · Stripe, *Webhooks*: https://docs.stripe.com/webhooks · Google, *API Improvement Proposals*: https://google.aip.dev/
- *Semantic Versioning*: https://semver.org/lang/pt-BR/ · Brasil, Lei nº 13.709/2018 (LGPD): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
