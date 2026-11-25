# Fluxo de trabalho entre agentes (SOP)

> VTX-010 · Fase F1 · Base de Conhecimento. Procedimento operacional padrão de como o trabalho passa de um agente para outro em qualquer projeto da VTX. Os fluxos específicos por tipo de projeto (VTX-066 a 072) partem deste documento.

## 1. Princípios
1. **Passagem por artefato, não por conversa.** Cada etapa termina com um documento ou código salvo no repositório. O próximo agente lê o artefato, não o histórico (modelo de SOP do MetaGPT).
2. **Uma responsabilidade por etapa.** Cada etapa tem um dono (papel) e critérios de saída claros.
3. **Separação de autor e revisor.** Quem produz não aprova o próprio trabalho.
4. **Lotes pequenos.** Tarefas e PRs pequenos reduzem retrabalho e risco (DORA).
5. **Humano no controle.** Samuel aprova escopo, publicação em produção, gastos e qualquer comunicação externa.
6. **Contexto mínimo.** Cada agente carrega só a definição do seu papel, o artefato de entrada e os documentos da base que a tarefa pede.

A stack de cada tipo de projeto está na [matriz ferramenta × fluxo](../ferramentas/README.md#matriz).

## 2. Etapas padrão

| # | Etapa | Dono | Entrada | Saída (artefato) | Portão de saída |
|---|---|---|---|---|---|
| 0 | Triagem | Orquestrador | Pedido do Samuel | Ficha do projeto (tipo, objetivo, restrições) | Tipo e fluxo escolhidos (VTX-066) |
| 0.5 | Pesquisa de domínio (VTX-130) | Produto + Arquiteto | Ficha + entrevista | Base `projects/<p>/conhecimento/` ([pesquisa-de-dominio.md](pesquisa-de-dominio.md)) | Checklist da pesquisa completo |
| 1 | Requisitos | Produto | Ficha + base de domínio | PRD + histórias com critérios de aceite | **Aprovação do Samuel (escopo)** |
| 2 | Arquitetura | Arquiteto | PRD | Documento de arquitetura + ADRs | Revisão do Orquestrador; Segurança se houver dado sensível |
| 3 | Planejamento | Orquestrador | PRD + arquitetura | Issues pequenas, priorizadas, com dependências | Cada issue cabe em 1 PR |
| 4 | Implementação | Dev Backend / Frontend-Mobile | Issue | PR com código, testes e descrição | CI verde |
| 5 | Revisão e testes | QA | PR | Revisão + relatório de testes | Critérios de aceite atendidos |
| 6 | Publicação | DevOps/SRE | PR aprovado | Release em homologação/produção, notas de versão | **Aprovação do Samuel (produção)** |
| 7 | Operação e aprendizado | DevOps/SRE + Orquestrador | Release | Monitoramento, incidentes, retrospectiva | Lições registradas na base |

As etapas 4 e 5 se repetem por issue até o backlog do incremento acabar (ciclo curto, no estilo Scrum/Kanban).

## 3. Regras de passagem (handoff)
- **Formato:** toda passagem cita o artefato (caminho no repositório ou link da issue/PR), o que foi feito, o que falta e as dúvidas em aberto.
- **Definition of Ready (para começar):** entrada completa, critérios de aceite claros, dependências resolvidas.
- **Definition of Done (para entregar):** artefato salvo, critérios atendidos, testes passando, documentação mínima atualizada.
- **Devolução:** se a entrada estiver incompleta, o agente devolve à etapa anterior com a pergunta específica, sem adivinhar requisito.
- **Limite de tentativas:** após 2 ciclos de retrabalho na mesma issue, o Orquestrador escala ao Samuel ou ao Arquiteto.

## 4. Coordenação
- **Quadro único:** issues no GitHub com rótulos de etapa (`requisitos`, `arquitetura`, `dev`, `qa`, `deploy`) e de papel. O backlog diário alimenta o painel.
- **Limite de trabalho em andamento (WIP):** no máximo 1 tarefa ativa por agente; o Orquestrador só puxa nova tarefa quando a anterior sai da etapa.
- **Ritmo:** planejamento no início do incremento, status diário no backlog, retrospectiva no fim (Scrum Guide 2020).

## 5. Quando escalar ao Samuel
Mudança de escopo ou prazo · publicação em produção · custo ou serviço pago novo · dado pessoal ou sensível (LGPD) · conflito entre agentes sem consenso · bloqueio por mais de 1 dia.

## 6. Exemplo curto
Pedido: "sistema de agendamento para clínica". Triagem → tipo *sistema web*. Produto escreve o PRD com 12 histórias; Samuel aprova. Arquiteto registra ADR-001 (stack) e ADR-002 (autenticação). Orquestrador cria 15 issues. Dev Backend abre PR da API de horários; QA reprova por falta de teste de conflito de horário; Dev corrige; QA aprova. DevOps publica em homologação; Samuel aprova produção.

## 7. Checklist do Orquestrador
- [ ] Tipo de projeto e fluxo definidos
- [ ] PRD aprovado pelo Samuel
- [ ] Arquitetura e ADRs revisados
- [ ] Issues pequenas, com critérios de aceite e dono
- [ ] Nenhum PR aprovado pelo próprio autor
- [ ] Publicação em produção aprovada pelo Samuel
- [ ] Retrospectiva registrada na base

## Fontes
- Hong et al., *MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework* (2023): https://arxiv.org/abs/2308.00352
- Qian et al., *ChatDev: Communicative Agents for Software Development* (2023): https://arxiv.org/abs/2307.07924
- Schwaber & Sutherland, *The Scrum Guide* (2020): https://scrumguides.org/scrum-guide.html
- Google, *Engineering Practices: Code Review*: https://google.github.io/eng-practices/review/
- DORA, *Working in small batches*: https://dora.dev/capabilities/working-in-small-batches/
- Anderson, D., *Kanban* (2010) — limites de WIP e fluxo puxado.
