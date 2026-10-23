# Padrão de pagamentos

Decisão do Samuel (23/10/2026): **Stripe é o gateway principal** dos projetos VTX. Mercado Pago fica como alternativa quando o cliente exigir.

## Regras
1. **Dinheiro real é decisão do Samuel.** Agentes só usam modo de teste (`sk_test_`/chaves restritas). Ativar conta, modo live, taxas e contrato: Samuel.
2. **Chaves fora do repo e do chat.** Ficam no cofre do ambiente (variáveis da hospedagem / `.env` local ignorado). Manifestos registram só o local. Chave publicável no front; secreta só no servidor.
3. **Checkout hospedado primeiro** (Stripe Checkout / Payment Links): menos código, cartão não passa pelos nossos servidores (PCI mais simples).
4. **Webhooks:** verificar a assinatura (`Stripe-Signature` + segredo do endpoint) sempre; tratar eventos de forma idempotente (guardar `event.id`); o estado do pedido muda pelo webhook, não pelo redirect.
5. **Brasil:** cartão, boleto e Pix [A CONFIRMAR disponibilidade e taxas na conta BR]. Valores em centavos, moeda `brl`.
6. **Testes:** Stripe CLI local para encaminhar webhooks; cartões de teste; teste automático para cada evento tratado.
7. **MCP / Agent Toolkit da Stripe:** só com chave restrita de teste, permissões mínimas.

## Custos
Sem mensalidade; taxa por transação [A CONFIRMAR tabela BR vigente]. Modo de teste é grátis.
