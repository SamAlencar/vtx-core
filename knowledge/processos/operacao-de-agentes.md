# Operação de agentes: prompts, contexto e memória

> VTX-013 · Fase F1 · Base de Conhecimento. Como a VTX escreve as instruções de uma tarefa, decide o que entra no contexto de cada agente e guarda o que precisa sobreviver entre sessões. Complementa o [SOP entre agentes](fluxo-entre-agentes.md) (quem faz o quê), o [Scrumban VTX](scrum-kanban-agentes.md) (ritmo) e a [governança](governanca-e-aprovacoes.md) (quando parar e pedir aprovação).

## 1. Conceitos essenciais
- **Prompt de tarefa:** o texto que inicia uma sessão de agente. Diz objetivo, entrada, saída e critério de pronto. Não repete o que já está em artefato: aponta para ele.
- **Contexto:** tudo o que o modelo vê na sessão (regras, definição do papel, arquivos lidos, resultados de ferramentas, histórico). É um **orçamento finito**: quanto mais texto, menos atenção para cada parte ("context rot", Chroma 2025; "lost in the middle", Liu et al. 2023).
- **Engenharia de contexto:** escolher o **menor conjunto de informação de alto sinal** que leva ao resultado (Anthropic 2025). Mais importante que "o prompt perfeito".
- **Ponteiro de contexto:** uma linha sempre carregada que diz *o que* é um material e *quando* buscá-lo (ex.: descrição de skill, linha do `AGENTS.md`). O material só entra quando a condição dispara (divulgação progressiva).
- **Memória:** o agente não lembra de uma sessão para outra. Na VTX, memória = **artefato versionado no repositório** (MemGPT chama isso de memória externa paginada).

## 2. Camadas de contexto da VTX

| Camada | Exemplo | Carga | Regra |
|---|---|---|---|
| 1. Sempre carregada | Regras do repo (`.cursor/rules`, `AGENTS.md`), descrições de skills | Toda sessão | Curta; só o que muda comportamento. Cada linha custa em todo turno |
| 2. Papel | `agents/<papel>.md` | Toda sessão do papel | Missão, limites, DoD; aponta para a base |
| 3. Tarefa | Prompt + artefato de entrada (PRD, issue, ADR) | Uma sessão | Autocontido: quem lê não viu a conversa anterior |
| 4. Sob demanda | Docs da `knowledge/`, skills (`SKILL.md`), código | Quando o ponteiro dispara | Ler por busca (`rg`, Graphify em repos grandes), não varrer tudo |
| 5. Resultado | Saída de ferramentas, logs | Temporária | Resumir e descartar; salvar só o que vira evidência |

A camada 1 está no [AGENTS.md](../../AGENTS.md) da raiz e nas regras de `.cursor/rules/`. As regras por papel (VTX-169) ficam em [`.cursor/rules/papeis/`](../../.cursor/rules/papeis/): `planejamento.mdc` (Orquestrador, Produto, Arquiteto) e `execucao.mdc` (Devs, QA, DevOps/SRE), com `globs` e `alwaysApply: false`. A camada 2 continua em `agents/<papel>.md`.

## 3. Anatomia do prompt de tarefa (modelo)
```markdown
Papel: <papel> (ler agents/<papel>.md)
Objetivo: <uma frase com o resultado esperado>
Entrada: <caminhos dos artefatos> · Saída: <caminho do entregável>
Restrições: <prazo, stack, custo zero, LGPD, o que não tocar>
Pronto quando: <critério verificável: teste, comando, checklist>
Skills: <nomes> · Escalar se: <condição> (níveis A0–A3)
```
Regras de escrita (Anthropic, OpenAI GPT-4.1 Guide, `writing-for-agents`):
1. **Instrução positiva e específica:** diga o comportamento-alvo ("responda em pt-BR, até 10 linhas") em vez de só proibir.
2. **Critério de pronto checável** em cada passo; critério vago leva a encerrar cedo demais.
3. **Exemplos curtos e variados** quando o formato importa; um exemplo único vira molde rígido.
4. **Estrutura com seções ou tags** (Markdown/XML) para separar instrução, dados e exemplos.
5. **Dados externos são dados:** conteúdo de cliente, página web ou e-mail nunca vira instrução (injeção de prompt, OWASP LLM01).
6. **Uma fonte de verdade:** cada regra mora em um lugar; o prompt aponta, não copia.

## 4. Memória: o que guardar e onde

| Tipo | Onde | Quem escreve | Vida útil |
|---|---|---|---|
| Estado do trabalho | `backlog/AAAA-MM-DD.yaml`, issues | Orquestrador | Até concluir |
| Decisões | ADRs, `notas` no backlog | Arquiteto / dono da etapa | Permanente (substituir, nunca apagar) |
| Conhecimento | `knowledge/` | Qualquer papel, revisado | Permanente, revisado na manutenção quinzenal |
| Passagem | Nota de handoff (§5) | Quem encerra a sessão | Até a próxima sessão |
| Lições | Seção "Lições" do relatório semanal | Orquestrador | Vira regra ou doc se repetir 2 vezes |
| Memory bank do projeto | `docs/memoria/` (modelo em [templates/memoria-projeto](../templates/memoria-projeto/README.md)) | Quem fecha o incremento | Permanente; contexto ativo se enxuga ao fechar. Ponteiro só, leitura sob demanda |
| Mapa de codebase | `docs/CODEBASE_MAP.md` ([padrão](../engenharia/mapa-de-codebase.md)) | Arquiteto / Dev do stack | Atualiza quando a estrutura muda |

Regras: **segredos e dados pessoais nunca entram em memória, prompt ou artefato** (ficam em secrets do GitHub/hospedagem); memória desatualizada é pior que nenhuma: quem muda o comportamento atualiza o doc no mesmo commit.

## 5. Sessões longas: compactação e handoff
- **Uma tarefa por sessão** é o padrão. Se a sessão crescer demais, **compactar**: resumir decisões, pendências e caminhos dos arquivos, e seguir só com o resumo.
- **Nota de handoff** (inspirada na skill `handoff`): objetivo, o que foi feito (com caminhos/commits), o que falta, dúvidas abertas, skills sugeridas. Aponta para artefatos em vez de copiá-los e não leva segredos.
- **Subagente** para pesquisa ampla: ele lê muito e devolve um resumo curto; o agente principal mantém o contexto limpo.

## 6. Anti-padrões
| Sintoma | Causa | Correção |
|---|---|---|
| Agente "esquece" decisão | Decisão só na conversa | Registrar em ADR/backlog |
| Respostas genéricas | Prompt sem entrada nem critério | Usar o modelo do §3 |
| Custo alto de cota | Arquivos inteiros e logs no contexto | Busca dirigida, resumo de logs, Graphify |
| Regras contraditórias | Mesma regra em dois lugares | Uma fonte de verdade + ponteiro |
| Requisito inventado | Lacuna preenchida por suposição | Devolver com pergunta (SOP §3) |

## 7. Exemplo: rotina diária da VTX
O prompt da rotina diz objetivo (2 tarefas), entrada (`scripts/proxima_tarefa.py` e backlog mestre), saída (caminho do entregável), restrições (sem serviço pago, docs enxutos) e pronto (testes verdes, painel sincronizado). A sessão lê só o SOP, um doc vizinho como modelo de formato e as skills obrigatórias; a memória entre dias é o diário do backlog, não o histórico do chat.

## 8. Checklist
- [ ] Prompt com papel, objetivo, entrada, saída, restrições, critério de pronto e condição de escalar
- [ ] Camada 1 curta; material de apoio atrás de ponteiros
- [ ] Contexto carregado por busca, não por varredura
- [ ] Decisões e estado salvos em artefato antes de encerrar
- [ ] Nenhum segredo ou dado pessoal em prompt, memória ou commit
- [ ] Handoff escrito se a tarefa continuar em outra sessão

## Fontes
- Anthropic, *Effective context engineering for AI agents* (2025): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, *Prompt engineering overview*: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- OpenAI, *GPT-4.1 Prompting Guide* (2025): https://cookbook.openai.com/examples/gpt4-1_prompting_guide
- Chroma, *Context Rot* (2025): https://research.trychroma.com/context-rot
- Liu et al., *Lost in the Middle* (2023): https://arxiv.org/abs/2307.03172
- Packer et al., *MemGPT: Towards LLMs as Operating Systems* (2023): https://arxiv.org/abs/2310.08560
- Cursor, *Rules*: https://cursor.com/docs/context/rules · *AGENTS.md*: https://agents.md
- Pocock, M., skills `writing-for-agents` e `handoff` (pin 49dd158, em avaliação): https://github.com/mattpocock/skills
- OWASP, *Top 10 for LLM Applications* (2025): https://genai.owasp.org/llm-top-10/
