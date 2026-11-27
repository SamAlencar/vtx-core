# Topologia de agentes: orquestrador, subagentes e modelos por perfil

> VTX-221 · Fase F1 · Processo. Como a VTX divide o trabalho entre agentes dentro do Cursor: quem coordena, quem verifica, quando nasce um agente novo, que modelo usa cada perfil e onde fica cada instrução. Complementa os [papéis](../organizacao/papeis-de-agentes.md), o [SOP entre agentes](fluxo-entre-agentes.md) e a [operação de agentes](operacao-de-agentes.md). Mapeamento das orientações do Samuel: [orientacoes-agentes-ia.md](orientacoes-agentes-ia.md).

## 1. Conceitos

- **Agente faz-tudo** é o anti-padrão: um contexto só para planejar, implementar, testar e aprovar. Erra mais (contexto saturado) e aprova o próprio trabalho, o que é A3 na [governança](governanca-e-aprovacoes.md).
- **Orquestrador:** decompõe, delega, junta e decide o próximo passo. Não implementa nem aprova o que delegou.
- **Subagente:** sessão com contexto limpo, objetivo único e saída curta (artefato ou parecer). Some quando entrega.
- **Verificador:** subagente cuja saída é um veredito sobre o artefato de outro (revisão, teste, conferência de critério de aceite).

## 2. Padrão: orquestrador + subagentes que validam

1. O orquestrador lê o pedido e o backlog e quebra em tarefas com critério de pronto checável ([modelo de prompt](operacao-de-agentes.md)).
2. Cada tarefa vai para um executor (papel de execução) numa sessão própria. A passagem é por artefato: branch, PR, documento.
3. Um verificador com contexto limpo confere o artefato contra o critério de aceite, sem ver a conversa do executor. No vtx-core é o **Tzu**, que deixa o veredito no PR (ver [porta para produção](porta-para-producao.md)).
4. Achado do verificador volta ao executor; o orquestrador só junta quando há veredito favorável sobre a HEAD exata.
5. Pesquisa ampla também vai para subagente, que devolve resumo curto; o contexto do orquestrador fica limpo.

Limite: WIP = 1 por agente, como no [Scrumban VTX](scrum-kanban-agentes.md); paralelismo só entre agentes diferentes e dentro da cota semanal.

## 3. Agente novo × ferramenta ou subagente

| Pergunta | Se sim | Se não |
|---|---|---|
| A capacidade é independente da tarefa (vale igual em qualquer projeto)? | candidata a agente | subagente ou ferramenta |
| É reutilizada por vários papéis ou projetos? | candidata a agente | subagente da tarefa |
| Precisa de contexto limpo ou de permissão diferente da do executor (ex.: revisar sem poder escrever)? | agente | ferramenta do executor |
| Tem entrada e saída estáveis, descritas em artefato? | agente com `agents/<papel>.md` | ainda não: começar como subagente e observar |

Regra: só vira **agente** (arquivo em `agents/` ou papel no SOP) quem passa nas três primeiras. Exemplos: revisão de código e QA são agentes (independentes, reutilizáveis, contexto limpo). Extrair requisitos de um PDF do cliente é subagente da tarefa. Validar um IFC é **ferramenta** (`core/vtx_ifc`). Agente novo segue a [VTX-207](../../backlog/projeto.yaml) (só quando um projeto real mostrar a lacuna) e é decisão A1 registrada.

## 4. Modelos por perfil

| Perfil | Trabalho | Modelo |
|---|---|---|
| Planejamento e aceite | Critérios de aceite, arquitetura, ADR, decomposição | O mais forte disponível no plano |
| Verificação | Revisão cruzada, parecer de PR, auditoria | Forte e **diferente do que escreveu**, quando o plano oferecer mais de um |
| Execução guiada por testes | Implementação repetitiva com teste já escrito, ajuste de lint, migração mecânica | Rápido e barato |
| Pesquisa e resumo | Ler muito e devolver pouco | Rápido |

Limites: só modelos incluídos no plano do Cursor e na cota semanal do Grok Bot. Nada de uso sob demanda (extra) nem provedor pago novo (A2). Se a cota não der, a tarefa espera e o Samuel é avisado. O modelo usado entra nas `notas` do diário quando a escolha for relevante.

## 5. Instruções como código, por escopo

| Arquivo | Escopo | Carga |
|---|---|---|
| `AGENTS.md` (raiz) | Regras que valem para qualquer agente no repositório | Sempre; curto (até ~60 linhas, testado) |
| `AGENTS.md` em subpasta | Regras de uma camada de código (ex.: `src/dominio/`) | Quando o agente mexe na pasta. Entra no template web com a [VTX-212](../../backlog/projeto.yaml) |
| `.cursor/rules/*.mdc` | Regra por papel ou por tipo de arquivo (`globs`) | Quando o contexto combina |
| `agents/<papel>.md` | Missão, limites e DoD do papel | Sessões do papel |
| `.cursor/skills/<nome>/SKILL.md` | Procedimento reutilizável (como fazer X) | Sob demanda, pela descrição |
| `DESIGN.md` | Sistema de design do produto (tokens, componentes, tom) para quem gera interface | Só em repositório com UI. Entra no template web com a [VTX-210](../../backlog/projeto.yaml) |

Tudo isso é versionado no Git e muda por PR, como código. Uma regra mora num lugar só; os outros apontam para ela.

## 6. Exemplo

Pedido: "endpoint de agendamento no med-hub". O orquestrador cria duas tarefas. Arquiteto (modelo forte) escreve o critério de aceite e o ADR. Dev Backend (modelo rápido) implementa com os testes do critério. O Tzu (outro modelo, contexto limpo) revisa o PR e dá veredito na HEAD. O orquestrador junta depois do veredito e do CI verde.

## 7. Checklist

- [ ] Nenhuma sessão planeja, implementa e aprova a mesma entrega
- [ ] Verificador com contexto limpo e veredito na HEAD exata
- [ ] Agente novo passou nas três primeiras perguntas do §3 e foi registrado como A1
- [ ] Modelo escolhido pelo perfil, dentro da cota semanal, sem uso extra
- [ ] Instrução nova no arquivo do escopo certo (§5), sem cópia em outro lugar

## Fontes

- Anthropic, "Building effective agents" (2024): orchestrator-workers e evaluator-optimizer. https://www.anthropic.com/engineering/building-effective-agents
- Cursor, regras e `AGENTS.md`: https://cursor.com/docs/context/rules
- AGENTS.md (formato aberto, arquivos aninhados por pasta): https://agents.md/
