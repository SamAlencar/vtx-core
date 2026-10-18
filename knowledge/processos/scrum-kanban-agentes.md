# Scrum e Kanban adaptados a agentes

> VTX-012 · Fase F1 · Base de Conhecimento. Como a VTX organiza o ritmo de trabalho dos agentes de IA combinando Scrum (metas e cadência) e Kanban (fluxo puxado e limite de WIP). Complementa o [SOP entre agentes](fluxo-entre-agentes.md), que define as etapas e as passagens.

## 1. Conceitos essenciais
**Scrum** (Scrum Guide 2020): trabalho em Sprints de duração fixa com uma **Meta da Sprint**. Papéis: Product Owner (valor e prioridade), Scrum Master (eficácia do time) e Developers (entrega). Eventos: Planejamento, Daily, Revisão e Retrospectiva. Artefatos: Product Backlog, Sprint Backlog e Incremento, cada um com um compromisso (Meta do Produto, Meta da Sprint, Definition of Done).

**Kanban** (Kanban Guide 2020): otimizar o fluxo de valor com três práticas: **visualizar** o trabalho num quadro, **limitar o trabalho em andamento (WIP)** e **gerenciar ativamente** os itens em fluxo. Métricas: WIP, **throughput** (itens concluídos por período), **tempo de ciclo** (início → fim) e **idade do item** (há quanto tempo está aberto). Lei de Little: tempo de ciclo médio ≈ WIP médio ÷ throughput, ou seja, menos WIP dá entrega mais rápida.

## 2. O que muda quando o time é de agentes

| Aspecto | Time humano | Time de agentes VTX | Consequência |
|---|---|---|---|
| Capacidade | Horas e pessoas | **Cota semanal compartilhada** (tokens/sessões) | Planejar em tarefas por dia, não em horas |
| Memória | Lembra da conversa | Cada sessão começa do zero | Tudo passa por artefato no repositório |
| Velocidade | Limitada por cansaço | Rápida, mas erra com contexto ruim | Lotes pequenos e revisão obrigatória |
| Reuniões | Síncronas | Não existem | Eventos viram **arquivos** |
| Decisão final | Time / PO | **Samuel** (dono do produto) | Portões de aprovação explícitos |
| Risco típico | Atraso | Alucinação, retrabalho, escopo inventado | DoD rígida, autor ≠ revisor |

## 3. Modelo VTX (híbrido "Scrumban")
- **Cadência Scrum por fora:** incrementos de **1 semana** (sexta a sexta, alinhado ao resumo semanal), cada um com uma meta escrita em uma frase.
- **Fluxo Kanban por dentro:** dentro do incremento, o trabalho é puxado em ordem de prioridade, um item por vez por agente.
- **Papéis:**
  - *Product Owner* = **Samuel** decide escopo e prioridade; o agente **Produto** prepara e refina o backlog para ele.
  - *Scrum Master / gestor de fluxo* = **Orquestrador**: cuida do quadro, WIP, bloqueios e cadência.
  - *Developers* = Arquiteto, Dev Backend, Dev Frontend-Mobile, QA, DevOps/SRE e especialistas.
- **Quadro** (colunas = etapas do SOP): `A fazer` → `Requisitos` → `Arquitetura` → `Dev` → `QA` → `Aprovação Samuel` → `Concluído`. No vtx-core o quadro é o `backlog/` + painel; nos projetos de cliente, GitHub Projects/Issues (gratuito).

## 4. Eventos adaptados (assíncronos, por artefato)

| Evento | Como acontece na VTX | Artefato |
|---|---|---|
| Planejamento | Orquestrador escolhe a meta e os itens que cabem na cota da semana | Meta + lista de ids no resumo semanal |
| Daily | Cada rotina diária registra o que fez e bloqueios | `backlog/AAAA-MM-DD.yaml` |
| Refinamento | Produto quebra itens grandes e completa critérios de aceite antes de entrarem em `Dev` | Backlog mestre atualizado |
| Revisão | Demonstração do incremento ao Samuel com links | Resumo semanal (Drive + painel) |
| Retrospectiva | 3 perguntas: o que funcionou, o que travou, o que mudar; 1 ação concreta | Seção "Lições" no relatório semanal |

## 5. Regras de fluxo
1. **WIP = 1 por agente** e no máximo 2 itens em `Aprovação Samuel` por projeto; se encher, o fluxo para e o Orquestrador escala.
2. **Puxar, não empurrar:** um item só avança quando a etapa seguinte tem vaga e a DoD da etapa atual foi cumprida.
3. **Definition of Ready:** critérios de aceite, dependências resolvidas, entregável e caminho definidos.
4. **Definition of Done:** artefato salvo, testes/CI verdes (skill `verification-before-completion`), revisado por outro papel, backlog diário atualizado.
5. **Item grande demais** (não cabe numa sessão) volta para refinamento e é dividido.
6. **Bloqueado há mais de 1 dia** → pular para o próximo item e registrar; escalar se for decisão do Samuel.
7. **Sem story points.** Tamanho em P/M/G (P = 1 sessão, M = 2, G = dividir). Previsão por throughput real (itens/semana), não por estimativa.

## 6. Métricas acompanhadas (semanal)
- **Throughput:** tarefas concluídas na semana (meta atual: 14 = 2/dia).
- **Progresso e previsão:** restantes ÷ throughput = semanas até o fim, comparado com o prazo.
- **Idade dos itens** em andamento ou aguardando aprovação (alerta acima de 3 dias).
- **Retrabalho:** itens que voltaram de QA/aprovação (meta: < 20%).
- **Consumo de cota:** % da cota semanal usada; acima de 70% antes de quinta → reduzir ritmo (acordo com o Tek).

## 7. Exemplo: o próprio backlog da VTX
Em 18/10/2026: 24 de 129 tarefas concluídas, throughput de 2/dia (14/semana). Restam 105 → cerca de 7,5 semanas → término previsto por volta de 10/12/2026, antes da meta de início de janeiro. Se o Samuel acrescentar tarefas ou a cota apertar (VTX cai para 1/dia), a previsão é recalculada no resumo semanal e o atraso é comunicado com antecedência.

## 8. Checklist do Orquestrador
- [ ] Meta da semana escrita em uma frase
- [ ] Quadro reflete o estado real (diário do dia salvo e painel sincronizado)
- [ ] Nenhum agente com mais de 1 item ativo
- [ ] Itens em `Dev` têm critérios de aceite (DoR)
- [ ] DoD verificada com evidência antes de marcar concluído
- [ ] Throughput, previsão e cota registrados no resumo semanal
- [ ] Retrospectiva com 1 ação de melhoria

## Fontes
- Schwaber, K.; Sutherland, J. *The Scrum Guide* (2020): https://scrumguides.org/scrum-guide.html
- Vacanti, D.; Coleman, Y. *The Kanban Guide* (2020): https://kanbanguides.org/
- Scrum.org, *The Kanban Guide for Scrum Teams*: https://www.scrum.org/resources/kanban-guide-scrum-teams
- Anderson, D. *Kanban: Successful Evolutionary Change for Your Technology Business* (2010).
- Little, J. D. C. *A Proof for the Queuing Formula L = λW* (1961), Operations Research 9(3).
- DORA, *Working in small batches*: https://dora.dev/capabilities/working-in-small-batches/
- Anthropic, *Building effective agents* (2024): https://www.anthropic.com/research/building-effective-agents
- Hong et al., *MetaGPT* (2023): https://arxiv.org/abs/2308.00352
