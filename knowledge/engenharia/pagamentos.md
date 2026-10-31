# Padrão de pagamentos

Decisão do Samuel (23/10/2026): **Stripe é o gateway principal** dos projetos VTX. Mercado Pago fica como alternativa quando o cliente exigir.

## Regras
1. **Dinheiro real é decisão do Samuel.** Agentes só usam modo de teste (`sk_test_`/chaves restritas). Ativar conta, modo live, taxas e contrato: Samuel.
2. **Chaves fora do repo e do chat.** Ficam no cofre do ambiente (variáveis da hospedagem / `.env` local ignorado). Manifestos registram só o local. Chave publicável no front; secreta só no servidor.
3. **Checkout hospedado primeiro** (Stripe Checkout / Payment Links): menos código, cartão não passa pelos nossos servidores (PCI mais simples).
4. **Webhooks:** verificar a assinatura (`Stripe-Signature` + segredo do endpoint) sempre; tratar eventos de forma idempotente (guardar `event.id`); o estado do pedido muda pelo webhook, não pelo redirect.
5. **Brasil:** cartão e boleto liberados; Pix na Stripe só por convite para empresa BR (alternativa: Mercado Pago). Valores em centavos, moeda `brl`. Detalhes na [ficha](../ferramentas/pagamentos/stripe-mercado-pago.md).
6. **Testes:** Stripe CLI local para encaminhar webhooks; cartões de teste; teste automático para cada evento tratado.
7. **MCP / Agent Toolkit da Stripe:** só com chave restrita de teste, permissões mínimas.

## Custos
Sem mensalidade. Stripe BR (31/10/2026): cartão nacional 3,99% + R$ 0,39, boleto R$ 3,45, Pix 1,19% (convite). Tabela comparada com Mercado Pago na [ficha](../ferramentas/pagamentos/stripe-mercado-pago.md). Modo de teste é grátis.
