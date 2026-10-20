# Fluxo de entrevista com o cliente (descoberta)

> VTX-084 · Fase F1 · Base de Conhecimento. Detalha a **entrevista de descoberta** que alimenta a etapa de Produto do [SOP entre agentes](../fluxo-entre-agentes.md), logo após a [triagem](triagem.md). Vale para todos os tipos de projeto. Primeira aplicação: piloto `plataforma-projetos`, com o Samuel como cliente.

## 1. Conceitos
- **Descoberta (discovery):** entender problema, usuários, objetivos e restrições **antes** de decidir a solução. Saída: briefing/visão validado e backlog inicial.
- **Elicitação:** técnica do BABOK (IIBA) e do IREB para obter requisitos com as partes interessadas. A entrevista é a técnica principal; complementam-se com observação, análise de documentos e workshops.
- **Jobs to be Done (JTBD):** o cliente "contrata" um produto para fazer um progresso numa situação (Christensen). Ulwick (ODI) transforma o job em resultados desejados mensuráveis.
- **The Mom Test (Fitzpatrick):** perguntar sobre **a vida e o comportamento passado** do cliente, não sobre a sua ideia; fatos e compromissos valem mais que elogios e opiniões.
- **Lean Inception (Paulo Caroli):** sequência curta de atividades para alinhar visão, escopo do MVP e ordem de entrega (visão, é/não é/faz/não faz, personas, jornadas, funcionalidades, revisão técnica, sequenciador, canvas MVP).
- **MoSCoW:** priorização em Must, Should, Could, Won't (desta vez).
- **Teoria × prática:** a teoria pressupõe um cliente disponível, uma sessão estruturada e respostas objetivas. Na prática o cliente chega com a solução pronta, mistura problema e funcionalidade, tem pouco tempo e responde aos poucos. O fluxo abaixo mostra as duas coisas em cada etapa.

## 2. Papéis
| Papel | Responsabilidade na entrevista |
|---|---|
| **Produto** (lidera) | prepara o roteiro, conduz, sintetiza, escreve briefing/visão e backlog inicial |
| **Arquiteto** (apoia) | levanta restrições técnicas, integrações, volumes, dados sensíveis; revisa viabilidade antes da validação |
| **Orquestrador** | dispara a entrevista após a triagem, garante os portões, registra no backlog e informa o Samuel |
| **Samuel** | aprova o briefing/visão (portão de saída). No piloto, também é o cliente |

## 3. Metodologia (passo a passo)

### Etapa 1 — Preparação
- **Teoria:** estudar o domínio, as partes interessadas e documentos existentes; escrever hipóteses (problema, usuário, valor) e o objetivo da sessão; montar um roteiro aberto (BABOK: "prepare for elicitation").
- **Prática:** 30–60 min de pesquisa (concorrentes, regulação, termos do setor). Escrever **3 hipóteses principais** e as **3 coisas que precisamos sair sabendo**. Adaptar o roteiro da seção 4: cortar blocos já respondidos pela triagem.
- **Saída:** roteiro adaptado + lista de hipóteses.

### Etapa 2 — Abertura e rapport
- **Teoria:** explicar objetivo, duração, como as respostas serão usadas; criar confiança.
- **Prática:** uma mensagem curta: "vou fazer perguntas em blocos, não existe resposta errada, 'não sei' é uma ótima resposta". Pedir permissão para registrar. Começar pelo contexto do cliente, nunca pela solução.

### Etapa 3 — Contexto e problema (JTBD + Mom Test)
- **Teoria:** descobrir o job (funcional, emocional, social), a situação em que surge, como é resolvido hoje e quanto custa. Perguntar sobre fatos passados e específicos; evitar perguntas indutivas ("você não acha que...?") e hipotéticas ("você usaria...?").
- **Prática:** o cliente vai falar de funcionalidades. Devolver com "**por que** isso é importante?" e "**qual foi a última vez** que isso aconteceu?". Elogios ("ia ser ótimo") não contam como evidência; procurar dinheiro, tempo ou esforço já gastos.

### Etapa 4 — Usuários e personas
- **Teoria:** identificar todos os grupos de usuários e partes interessadas (inclusive quem paga, quem usa, quem aprova, quem regula); descrever personas com objetivos e dores.
- **Prática:** limitar a 2–4 personas no MVP. Em plataformas com dois lados (marketplace), tratar cada lado separadamente e perguntar qual lado é mais difícil de atrair.

### Etapa 5 — Objetivos e métricas de sucesso
- **Teoria:** objetivos de negócio mensuráveis (SMART), resultados desejados (ODI) e critérios de aceite do projeto.
- **Prática:** perguntar "como você vai saber, daqui a 6 meses, que deu certo?". Converter respostas vagas ("muitos clientes") em números provisórios e marcar como hipótese.

### Etapa 6 — Escopo e MVP (Lean Inception)
- **Teoria:** frase de visão do produto; quadro é/não é/faz/não faz; funcionalidades a partir das jornadas; revisão técnica (esforço, valor, incerteza); sequenciador em ondas; canvas MVP.
- **Prática:** por chat, fazer versões leves: Produto propõe uma frase de visão e o quadro é/não é a partir das respostas, e o cliente corrige. O sequenciador é feito pelo Produto + Arquiteto depois da entrevista e validado com o cliente.

### Etapa 7 — Restrições
- **Teoria:** orçamento, prazo, regulação, segurança e privacidade, integrações, plataformas, requisitos não funcionais (IREB: requisitos de qualidade e restrições).
- **Prática:** orçamento e prazo costumam vir como "o mais barato/rápido possível"; oferecer faixas para escolha. Sempre perguntar sobre **dados pessoais (LGPD)** e **regras de conselhos/órgãos** do setor. O Arquiteto anota tudo que muda a arquitetura.

### Etapa 8 — Modelo de negócio
- **Teoria:** proposta de valor, segmentos, canais, receitas e custos (Business Model Canvas / Lean Canvas).
- **Prática:** focar em quem paga, quanto, quando e como o dinheiro circula. Em marketplace: comissão, assinatura ou taxa fixa, e quem recebe o quê.

### Etapa 9 — Riscos e premissas
- **Teoria:** levantar riscos de valor, usabilidade, viabilidade técnica e de negócio (Cagan) e premissas a validar.
- **Prática:** perguntar "o que faria isso dar errado?" e "o que você está assumindo que é verdade?". Ordenar por impacto × incerteza; os 3 maiores viram experimentos do MVP.

### Etapa 10 — Priorização (MoSCoW)
- **Teoria:** classificar requisitos em Must/Should/Could/Won't com o cliente.
- **Prática:** o cliente marca tudo como Must. Limitar: **no máximo ~60% do esforço em Must** (orientação do DSDM). Perguntar "se só pudesse ter 3 coisas no lançamento, quais seriam?".

### Etapa 11 — Fechamento e próximos passos
- **Teoria:** resumir o entendido, confirmar lacunas, combinar prazo da síntese e validação.
- **Prática:** última pergunta fixa: "**o que eu deveria ter perguntado e não perguntei?**". Combinar quando o cliente recebe o briefing.

### Depois da entrevista
1. **Síntese (Produto, até 1 dia):** organizar respostas por bloco; separar **fatos**, **opiniões** e **hipóteses**; listar lacunas e contradições.
2. **Revisão técnica (Arquiteto):** viabilidade, restrições, riscos técnicos, estimativa grossa (camisetas P/M/G).
2a. **Pesquisa de domínio (VTX-130, planejada):** antes do briefing/PRD, pesquisar o tema do serviço do cliente e montar `projects/<p>/conhecimento/`, reaproveitando a base existente do domínio — ver [pesquisa-de-dominio.md](../pesquisa-de-dominio.md).
3. **Artefatos:** briefing/documento de visão (visão, personas, problema/JTBD, objetivos e métricas, escopo é/não é, MVP, restrições, modelo de negócio, riscos, MoSCoW) e **backlog inicial** (épicos e histórias do Must).
4. **Validação com o cliente:** enviar o briefing e pedir correções explícitas por seção; repetir até "de acordo".
5. **Portões:**
   - **P0 — entrada:** triagem feita, roteiro adaptado (Orquestrador).
   - **P1 — síntese completa:** todos os blocos respondidos ou com lacuna registrada (Produto).
   - **P2 — viabilidade:** revisão do Arquiteto sem bloqueios abertos.
   - **P3 — aprovação do Samuel:** briefing/visão aprovado → segue o fluxo do tipo de projeto.

## 4. Roteiro de perguntas (pronto para uso)
Perguntas abertas, uma ideia por pergunta. Adaptar termos ao projeto.

**Bloco 1 — Contexto e problema**
1. Conte a história: o que te fez ter essa ideia? Que situação real você viu ou viveu?
2. Hoje, como uma pessoa que precisa de um projeto de engenharia ou arquitetura resolve isso? Passo a passo.
3. Qual foi a última vez que você (ou alguém próximo, ou um cliente seu) passou por isso? O que aconteceu?
4. O que é mais difícil, demorado ou caro nesse processo atual?
5. Quanto essas pessoas gastam hoje (dinheiro e tempo) para conseguir um projeto?
6. E do lado dos profissionais: como eles conseguem clientes hoje, e o que mais os incomoda nisso?
7. Já existe alguma solução parecida que você conheça? O que ela faz bem e mal?

**Bloco 2 — Usuários e personas**
Quem são os clientes (perfil, região, renda, tipo de obra)? Quem são os profissionais? Quem mais participa (prefeitura, conselhos, construtora, financiamento)? Qual lado é mais difícil de atrair? Quem decide e quem paga?

**Bloco 3 — Objetivos e métricas**
O que é sucesso em 6 e em 12 meses? Que números indicariam isso (projetos/mês, faturamento, profissionais ativos, nota de satisfação)? O que seria um resultado decepcionante?

**Bloco 4 — Visão e escopo do MVP**
Complete: "Para ___, que ___, a plataforma é ___ que ___; diferente de ___". O que a plataforma é e não é? Faz e não faz? Qual a menor versão que já gera valor real? Qual tipo de projeto e qual região no início?

**Bloco 5 — Jornadas e funcionalidades**
Descreva a jornada do cliente, do primeiro acesso à entrega. Descreva a do profissional, do cadastro à assinatura da ART/RRT. Como os projetos são distribuídos? O que acontece quando o profissional pede correções?

**Bloco 6 — Restrições**
Orçamento e prazo disponíveis (faixas)? Regras do CONFEA/CREA e CAU que preocupam? Que dados pessoais e do imóvel serão coletados (LGPD)? Integrações necessárias (pagamento, assinatura digital, consulta de registro profissional, Tekto)? Web, app ou ambos?

**Bloco 7 — Modelo de negócio**
Quem paga, quanto e quando? Como o valor é dividido entre plataforma e profissional? Pagamento retido até a entrega? Custos principais? Como os primeiros clientes e profissionais vão chegar?

**Bloco 8 — Riscos e premissas**
O que faria isso dar errado? O que você está assumindo como verdade sem ter testado? O que acontece se um projeto revisado tiver erro?

**Bloco 9 — Priorização (MoSCoW)**
Se só pudesse ter 3 funcionalidades no lançamento, quais? Classifique a lista proposta em Must/Should/Could/Won't.

**Bloco 10 — Fechamento**
O que eu deveria ter perguntado e não perguntei? Há documentos, referências ou pessoas que eu deveria consultar? Quando você pode revisar o briefing?

## 5. Modo assíncrono por chat (um bloco por vez)
- **Um bloco por mensagem**, numerado; o cliente responde no seu tempo, em texto ou áudio, inclusive parcialmente.
- **Antes do próximo bloco:** resumir em 2–4 linhas o que foi entendido e fazer até 2 perguntas de aprofundamento ("por quê?", "me dá um exemplo?"). Só avançar quando o cliente confirmar o resumo.
- **Respostas curtas são aceitas:** "não sei" vira lacuna registrada, não bloqueio.
- **Registro:** respostas consolidadas no repositório do projeto (ex.: `docs/entrevista.md`) a cada bloco, para nada se perder entre sessões.
- **Ritmo:** 1–2 blocos por dia; avisar quantos faltam ("bloco 3 de 10").
- **Prática:** no chat o cliente tende a responder com soluções e listas; reforçar perguntas sobre fatos e exemplos. Propor rascunhos (visão, é/não é) para o cliente corrigir é mais rápido que pedir para ele escrever do zero.

## 6. Exemplo — piloto `plataforma-projetos`
Hipóteses iniciais: (1) clientes de residências pequenas acham projeto caro e demorado; (2) profissionais aceitam revisar e assinar projetos gerados por IA mediante remuneração; (3) a regulação permite o modelo se o profissional for o responsável técnico. Precisamos sair sabendo: perfil do primeiro cliente, modelo de remuneração do profissional e escopo do MVP (residência térrea pequena: arquitetura, estrutura e fundação, conforme `docs/TEKTO.md`). Aplicação por chat, bloco a bloco, com o Samuel.

## 7. Checklist
- [ ] Triagem feita e roteiro adaptado; hipóteses e "3 coisas a saber" escritas
- [ ] Abertura enviada (objetivo, formato, registro)
- [ ] Problema descrito com fatos passados, não só opiniões
- [ ] Personas de todos os lados identificadas
- [ ] Objetivos com métricas (mesmo provisórias)
- [ ] Visão, é/não é e MVP rascunhados e corrigidos pelo cliente
- [ ] Restrições: orçamento, prazo, regulação, LGPD, integrações
- [ ] Modelo de negócio e riscos levantados
- [ ] MoSCoW com Must limitado
- [ ] Pergunta final feita; lacunas registradas
- [ ] Síntese, revisão técnica, briefing e backlog inicial prontos
- [ ] Briefing validado pelo cliente e aprovado pelo Samuel (P3)

## 8. Fontes
- IIBA. *BABOK Guide v3* — áreas de Elicitação e Colaboração; técnicas de entrevista e workshop. https://www.iiba.org/business-analysis-standards/babok-guide/
- IREB. *CPRE Foundation Level — Syllabus* (elicitação, tipos de requisitos). https://cpre.ireb.org/
- CAROLI, Paulo. *Lean Inception: como alinhar pessoas e construir o produto certo*. https://caroli.org/livro-lean-inception/
- FITZPATRICK, Rob. *The Mom Test*. https://www.momtestbook.com/
- CHRISTENSEN, C. et al. *Competing Against Luck* (Jobs to be Done), 2016; e "Know Your Customers' Jobs to Be Done", HBR, 2016.
- ULWICK, Anthony. *Jobs to be Done: Theory to Practice* (Outcome-Driven Innovation). https://jobs-to-be-done-book.com/
- Agile Business Consortium. *DSDM — MoSCoW Prioritisation*. https://www.agilebusiness.org/dsdm-project-framework/moscow-prioririsation.html
- OSTERWALDER, A.; PIGNEUR, Y. *Business Model Generation*; MAURYA, A. *Running Lean* (Lean Canvas).
- CAGAN, Marty. *Inspired* — quatro riscos de produto.
- Lei 13.709/2018 (LGPD). https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

Resumos próprios; nenhum trecho de fonte paga foi copiado.
