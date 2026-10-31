# Stripe e Mercado Pago
> Pagamentos · Status: **Stripe adotado (principal)**, Mercado Pago alternativa · Revisado em 2026-10-31 · VTX-106

## 1. O que é
**Stripe:** plataforma de pagamentos com API, Checkout hospedado, Payment Links, Billing (assinaturas), Connect (marketplaces), CLI e SDKs open source (MIT). **Mercado Pago:** gateway do Mercado Livre, muito usado no Brasil, com Checkout Pro (redireciona), Checkout Transparente (no site) e assinaturas. As regras gerais estão no [padrão de pagamentos](../../engenharia/pagamentos.md).

## 2. Quando usar / quando não usar
- **Stripe (padrão):** cartão nacional e internacional, assinaturas, marketplace com repasse (Connect), boleto.
- **Mercado Pago:** cliente que exige Pix sem convite da Stripe, já tem conta MP, ou cujo público paga com saldo MP/parcelado sem cartão.
- **Não usar:** guardar dados de cartão no nosso servidor (sempre checkout/elemento do provedor); dinheiro real antes de aprovação do Samuel.

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Stripe | padrão VTX | melhor API e docs, Checkout, CLI de webhooks |
| Mercado Pago | Pix essencial ou cliente MP | Pix 0,99% liberado na hora |
| Asaas / Pagar.me | só se o cliente já usar | não avaliados; ADR antes |

## 4. Custo (conferido em 31/10/2026, sem mensalidade)
| Meio | Stripe (conta BR, preço padrão) | Mercado Pago (Checkout Pro) |
|---|---|---|
| Cartão nacional | 3,99% + R$ 0,39 | 4,98% na hora; 4,49% em 14 dias; 3,98% em 30 dias |
| Cartão internacional | +2% | — |
| Pix | 1,19%, **só por convite** para empresa BR | 0,99% na hora |
| Boleto | R$ 3,45 (confirma em até 1 dia útil) | R$ 3,49 (até 3 dias) |
| Contestação | R$ 55,00 recebida + R$ 55,00 se contestar | conforme regras MP |
Billing da Stripe: 0,7% do volume. Modo de teste/sandbox dos dois é grátis. Taxas mudam: conferir na revisão trimestral.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | assinaturas | Stripe Billing + Customer Portal |
| [Mobile](../../processos/fluxos/app-mobile.md) | compra de bem/serviço físico | Stripe; bens digitais seguem regras das lojas |
| [API](../../processos/fluxos/api-integracoes.md) | integração | webhooks assinados e idempotentes |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | validar venda | Payment Links (sem código) |

## 6. Papel responsável
Arquiteto escolhe gateway por ADR; Dev Backend faz checkout, webhooks e conciliação; QA testa cada evento no modo de teste; DevOps guarda chaves; Samuel ativa conta live, aceita taxas e contrato ([papéis](../../../agents/)).

## 7. Setup
1. Conta em modo de teste; chaves `sk_test_`/restritas no `.env` local ignorado e no cofre da hospedagem.
2. Checkout hospedado ou Payment Element; valores em centavos, moeda `brl`; boleto ativado nas configurações de formas de pagamento.
3. Webhook com verificação de `Stripe-Signature`; `stripe listen --forward-to localhost:3000/api/webhooks` no desenvolvimento.
4. Mercado Pago: credenciais de teste e usuários de teste; notificações (webhook) com validação de assinatura `x-signature`.
5. MCP/Agent Toolkit da Stripe só com chave restrita de teste.

## 8. Segredos e segurança/LGPD
- Chave secreta e segredo de webhook só no servidor; chave publicável no front. Nunca no repo nem no chat.
- Pedido muda de estado **pelo webhook**, nunca pelo redirect; guardar `event.id` para idempotência.
- CPF/CNPJ do pagador (exigido no boleto) é dado pessoal: minimizar, só o necessário na nota fiscal; o cartão nunca passa pelo nosso servidor (PCI SAQ A).
- Boleto não tem reembolso pela Stripe: devolução fora da plataforma, registrada.

## 9. Checklist
- [ ] ADR do gateway (Stripe padrão; MP justificado)
- [ ] Só chaves de teste até aprovação do Samuel
- [ ] Webhook assinado, idempotente, com teste automático por evento
- [ ] Boleto assíncrono tratado (pendente, pago, vencido)
- [ ] Pix: convite Stripe confirmado ou MP no ADR
- [ ] Taxas repassadas ao preço do cliente e aprovadas

## 10. Registro de avaliação e Fontes
**ADR curto (31/10/2026):** *Contexto:* decisão do Samuel de 23/10 (Stripe principal). *Opções:* só Stripe, Stripe + MP, só MP. *Decisão:* Stripe padrão; MP quando o Pix for essencial e a Stripe não liberar o convite, ou o cliente exigir. *Consequência:* duas integrações possíveis, mesmas regras de webhook e chaves.
- Preços Stripe BR: https://stripe.com/br/pricing
- Formas locais (Pix, boleto): https://stripe.com/br/pricing/local-payment-methods
- Boleto na Stripe: https://docs.stripe.com/payments/boleto
- Pix na Stripe: https://docs.stripe.com/payments/pix
- Webhooks: https://docs.stripe.com/webhooks
- Stripe CLI: https://docs.stripe.com/stripe-cli
- Mercado Pago checkouts e taxas: https://www.mercadopago.com.br/ferramentas-para-vender/check-out
- Taxas MP (assinaturas): https://www.mercadopago.com.br/ajuda/19495
- Notificações MP: https://www.mercadopago.com.br/developers/pt/docs/your-integrations/notifications/webhooks
