# ADR-004: Seguro cobrado pela corretora parceira, fora da plataforma
- **Status:** aceito (decisão do Samuel em 18/10/2026, [etapa 1](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/etapa1-escopo.md))
- **Data:** 20/10/2026 · **Nível de governança:** A2 (aprovado)

## Diagrama
Encaminhamento à corretora: [0004-seguro-cobrado-pela-corretora.html](diagramas/0004-seguro-cobrado-pela-corretora.html).

## Contexto
A plataforma antiga vendia e cobrava seguros pelo Stripe (`insurance_subscriptions`, preços customizados). O Samuel decidiu que esse modelo não continua e que a cobrança é feita pelo método da corretora parceira.

## Decisão
A plataforma só **mostra** os seguros indicados e **encaminha** o médico à corretora (link ou WhatsApp). Não há preço, compra, apólice nem cobrança de seguro na 4med.co. O seguro não faz parte do plano de R$ 599.

## Alternativas
- **Vender dentro da plataforma:** recusada. Exigiria registro de corretor na SUSEP e envolveria cobrança e dados de apólice.

## Consequências
- (+) A 4med.co não atua como corretora; intermediar seguro exige registro na SUSEP (Lei 4.594/1964; Decreto-Lei 73/1966) [A CONFIRMAR com o parceiro se a simples indicação remunerada precisa de algum enquadramento].
- (+) Menos dados pessoais e menos integrações.
- (−) A comissão por indicação, se houver, depende de controle fora da plataforma (#22 fica para depois).
