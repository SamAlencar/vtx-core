# Fluxo de projeto: MVP / prova de conceito

> VTX-072 · Fase F1 · Base de Conhecimento. Especializa o [SOP entre agentes](../fluxo-entre-agentes.md) para projetos cujo objetivo é **aprender antes de investir**. Vale quando a [triagem](triagem.md) define `tipo_principal: mvp-poc` (prazo fixo, escopo variável, incerteza alta). O fluxo do produto final ([SaaS](sistema-web-saas.md), [app](app-mobile.md), [API](api-integracoes.md), [site](site-landing-page.md)) entra como módulo técnico. A descoberta segue a [entrevista com o cliente](entrevista-cliente.md).

## 1. Conceitos
- **PoC (prova de conceito):** responde "**dá para fazer?**" — risco técnico (ex.: a IA gera uma planta válida? a API do órgão aceita integração?). Público interno; código descartável.
- **Protótipo:** responde "**como seria?**" — fluxo e interface, de papel a alta fidelidade, sem lógica real. Serve para testar entendimento e usabilidade.
- **MVP (produto mínimo viável):** responde "**alguém quer e paga?**" — a menor versão que permite o ciclo *construir → medir → aprender* com usuários reais (Ries). Mínimo no escopo, não na qualidade do que entrega: deve ser utilizável, confiável e agradável no pouco que faz (Kniberg).
- **Piloto:** o produto (ou MVP) em uso real por um grupo restrito, com prazo e critério de saída.
- **Hipótese antes do código:** todo MVP/PoC parte de hipóteses escritas (valor, crescimento, viabilidade técnica) com métrica e critério de sucesso decididos **antes** do teste (*Test Card*, Strategyzer).
- **Prazo fixo, escopo variável:** define-se o "apetite" (quanto tempo/verba a ideia merece) e corta-se escopo para caber, nunca o contrário (Shape Up).
- **Tipos de MVP sem código pesado:** página de fumaça (landing + lista de espera), *concierge* (serviço feito à mão), Mágico de Oz (interface real, bastidor manual), recurso único, protótipo clicável. Usar o mais barato que responde à hipótese.
- **Arquitetura sacrificial:** aceitar conscientemente que o código do teste pode ser jogado fora (Fowler); a decisão "descartar ou evoluir" é explícita no fim.
- **Ferramentas:** padrão — GitHub Actions (CI mínimo), Cursor, Stripe (Payment Links, se houver venda). O restante é opcional e de baixo custo (Supabase Free, Cloudflare, Figma, Expo Go, Vercel Hobby só sem receita). Detalhe na [matriz ferramenta × fluxo](../../ferramentas/README.md#matriz).

## 2. Etapas do fluxo

| # | Etapa | Papéis | Artefatos | Portão |
|---|---|---|---|---|
| 0 | Triagem | Orquestrador | `projects/<p>/ficha.yaml` com incerteza (requisitos x tecnologia) e prazo | `tipo_principal: mvp-poc` |
| 1 | Descoberta enxuta | Produto | Entrevista com o cliente, problema, público, alternativas atuais | Problema e público descritos em 1 página |
| 2 | Hipóteses e critérios | Produto + Arquiteto | Lista de hipóteses priorizada por risco; *Test Card* de cada uma (métrica, alvo, prazo); critérios de "continuar / pivotar / parar" | **Samuel aprova hipóteses, critérios e apetite (prazo e custo)** |
| 3 | Desenho do experimento | Produto + Arquiteto + Dev | Tipo de MVP/PoC escolhido, escopo mínimo (MoSCoW só com *Must*), stack de baixo custo, plano de medição (eventos, analytics, roteiro de teste com usuário) | Escopo cabe no apetite |
| 4 | Construção em timebox | Dev + QA | Incrementos curtos; testes só no caminho crítico; segurança e LGPD básicos (HTTPS, segredos fora do código, consentimento) | Demo funcionando no prazo; nada de estender sem nova aprovação |
| 5 | Exposição e medição | Produto + DevOps | Usuários reais ou banca de teste, dados coletados, notas de entrevistas pós-uso | Período de medição completo |
| 6 | Aprendizado e decisão | Orquestrador + Produto + Arquiteto | Relatório: hipótese x resultado, evidências, custo real, recomendação (continuar, pivotar, parar) e destino do código (descartar ou evoluir) | **Samuel decide o próximo passo** |
| 7 | Transição | Orquestrador | Se continuar: nova triagem para o fluxo do produto, débitos técnicos listados, ADR "evoluir x reescrever". Se parar: aprendizado arquivado e recursos desligados | Ficha nova aberta ou projeto encerrado |

Ciclos curtos: um MVP pode repetir 3 → 6 várias vezes; cada volta testa a hipótese de maior risco restante.

## 3. Pontos de aprovação do Samuel
1. Hipóteses, critérios de sucesso e apetite (etapa 2). Sem critério escrito antes, o resultado não é aceito como prova.
2. Qualquer extensão de prazo ou verba na construção (etapa 4): prazo estourado é sinal para cortar escopo, não para crescer.
3. Exposição a usuários reais ou dados pessoais reais, cobrança de dinheiro e uso do nome do cliente em público (etapa 5).
4. A decisão final de continuar, pivotar ou parar, e se o código vira base do produto (etapa 6).

## 4. Itens específicos de MVP/PoC
- **Métricas acionáveis, não de vaidade:** conversão, retenção, disposição a pagar, tarefa concluída. Visitas e cadastros soltos não validam nada.
- **Qualidade mínima inegociável:** mesmo descartável, nada de segredo no repositório, dado pessoal sem consentimento ou sistema exposto sem autenticação.
- **Custo controlado:** preferir planos gratuitos, serviços gerenciados e ferramentas no-code/low-code; registrar cada custo recorrente para desligar no fim.
- **Débito técnico declarado:** tudo que foi feito "rápido" fica listado; se o MVP evoluir, essa lista vira backlog da etapa 7.
- **Contrato claro:** o cliente sabe que compra aprendizado em prazo fixo, não um produto pronto; entregáveis são o relatório e a demo.

## 5. Riscos típicos e mitigação

| Risco | Mitigação |
|---|---|
| MVP vira produto sem plano (código frágil em produção) | Decisão explícita na etapa 6; ADR "evoluir x reescrever"; débitos listados |
| Escopo cresce ("só mais essa função") | Apetite fixo; só *Must*; extensão exige aprovação do Samuel |
| Viés de confirmação (achar que deu certo) | Critérios escritos antes; dados brutos no relatório; revisão do Arquiteto |
| Testar com pessoas erradas | Público definido na descoberta; recrutar pelo perfil, não por conveniência |
| Construir quando um teste sem código bastava | Etapa 3 escolhe o MVP mais barato que responde à hipótese |
| Dado pessoal coletado sem base legal | Consentimento, mínimo de dados, apagar ao fim (LGPD) |

## 6. Exemplo
"Plataforma em que a IA gera um projeto de engenharia e um profissional credenciado revisa e assina a ART/RRT." Etapa 2: hipóteses de maior risco — (a) técnica: a IA gera uma planta/memorial que o revisor aceita com até 2 h de ajuste; (b) valor: 3 de 10 clientes entrevistados topam pagar um sinal. Apetite: 4 semanas. Etapa 3: PoC técnica para (a), com 5 casos reais anonimizados; MVP *concierge* para (b) — landing page e pedidos atendidos à mão. Etapa 6: (a) passou em 4 de 5 casos e (b) teve 2 sinais em 10; recomendação: pivotar o público para construtoras pequenas e repetir (b). Samuel decide.

## 7. Checklist de conclusão
- [ ] Problema e público descritos; entrevista registrada
- [ ] Hipóteses com métrica, alvo e prazo; critérios de continuar/pivotar/parar aprovados pelo Samuel
- [ ] Tipo de MVP/PoC justificado como o mais barato que responde à hipótese
- [ ] Construção dentro do apetite, sem extensão não aprovada
- [ ] Segredos protegidos, consentimento e mínimo de dados pessoais
- [ ] Medição completa; dados brutos e entrevistas pós-uso salvos
- [ ] Relatório de aprendizado com recomendação e destino do código
- [ ] Decisão do Samuel registrada; transição (nova ficha) ou encerramento com recursos desligados

## Fontes
- RIES, Eric. *The Lean Startup* — princípios e ciclo construir-medir-aprender: https://theleanstartup.com/principles · *Minimum Viable Product: a guide*: https://www.startuplessonslearned.com/2009/08/minimum-viable-product-guide.html
- KNIBERG, Henrik. *Making sense of MVP (Minimum Viable Product)*: https://blog.crisp.se/2016/01/25/henrikkniberg/making-sense-of-mvp
- Strategyzer. *The Test Card*: https://www.strategyzer.com/library/the-test-card
- Basecamp. *Shape Up*, cap. "Set Boundaries" (apetite, prazo fixo e escopo variável): https://basecamp.com/shapeup/1.2-chapter-03
- FOWLER, Martin. *Sacrificial Architecture*: https://martinfowler.com/bliki/SacrificialArchitecture.html
- GV. *The Design Sprint* (protótipo e teste em 5 dias): https://www.gv.com/sprint/
- Nielsen Norman Group. *UX Prototypes: Low Fidelity vs. High Fidelity*: https://www.nngroup.com/articles/ux-prototype-hi-lo-fidelity/
- CAROLI, Paulo. *Lean Inception* (canvas de MVP): https://caroli.org/livro-lean-inception/
- Brasil, Lei nº 13.709/2018 (LGPD): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

Resumos próprios; nenhum trecho de fonte paga foi copiado.
