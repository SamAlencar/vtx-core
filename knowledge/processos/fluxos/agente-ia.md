# Fluxo de projeto: agente de IA ou IA embutida

> VTX-198 · Fase F14 · Processo. Tipo de projeto em que a entrega principal é um agente (loop de tool-calling) ou uma IA embutida no produto. A triagem está em [triagem.md](triagem.md). Teto de custo no contrato é dependência externa (agentes de vendas), não aceite deste fluxo.

## 1. Conceitos

- **Agente:** um laço que recebe um objetivo, chama ferramentas, observa o resultado e para com critério explícito (máximo de iterações, timeout, erro interno).
- **IA embutida:** o produto (site, sistema ou API) chama um modelo para uma tarefa delimitada (classificar, redigir, extrair), sem necessariamente um laço aberto.
- Nos dois casos este fluxo **exige**, no plano do projeto, quatro peças técnicas: harness de referência (VTX-177), evals com portão no CI (VTX-178), telemetria de custo (VTX-179) e privacidade nos prompts (VTX-150). Sem isso o tipo não está completo. Enquanto essas quatro tarefas estiverem `a fazer` no vtx-core, um projeto para cliente externo só começa com A2 do Samuel, e o plano tem que incluir o equivalente das quatro peças no repositório do cliente (não esperar o core). Piloto interno segue o teto da F14: no máximo 1,5 h/semana do Samuel no piloto (critério de aceite da VTX-196 em [projeto.yaml](../../../backlog/projeto.yaml)), dentro das [5 h/semana da F14](../../../backlog/SCHEMA.md), com o trilho de receita primeiro; passar disso é A2.
- Hospedagem do app segue a [política de hospedagem por cliente](../../operacao/hospedagem-por-cliente.md) (VTX-195). Custo de token de plano pago é A2.

## 2. Metodologia (etapas)

| # | Etapa | Papéis | O que sai | Portão |
|---|---|---|---|---|
| 1 | Escopo e recorte | Produto + Orquestrador | PRD com tarefas do modelo, o que o agente *não* faz, e usuário dono da ação | Samuel aprova escopo |
| 2 | Arquitetura do laço | Arquiteto | ADR do harness: `max_iteracoes`, `timeout_s`, retry com backoff, fallback de modelo, parada em `ERRO_INTERNO` (VTX-177). Lista de ferramentas e permissões | A1 no ADR; ferramenta paga ou dado pessoal é A2 |
| 3 | Privacidade e dados | Arquiteto + Produto | Checklist da VTX-150: o que entra no prompt, retenção, se o provedor treina com os dados, base legal | Dado pessoal ou envio a provedor novo é A2 |
| 4 | Evals | QA + Dev | Conjunto mínimo de casos (entrada, ferramenta esperada, saída aceitável) e portão no CI (VTX-178). Roda sem rede e sem custo no CI, com cliente falso | CI vermelho impede merge |
| 5 | Telemetria de custo | DevOps + Dev | Contagem de tokens e chamadas por requisição/projeto (VTX-179), alerta quando passa do teto técnico de desenvolvimento | Plano pago do provedor é A2. Teto contratual com o cliente é dependência externa |
| 6 | Implementação | Dev | Laço, ferramentas e UI ou API no repositório do cliente. Testes do harness com cliente LLM falso | PR com CI verde, inclusive evals |
| 7 | Lançamento | DevOps + Orquestrador | Variáveis só no painel, runbook, deploy de produção | Deploy em produção é A2 (política de hospedagem) |
| 8 | Operação | DevOps + QA | Revisar evals quando o comportamento mudar; incidentes viram postmortem no repo do cliente | Nova ferramenta, novo provedor ou dado pessoal extra é A2 |

As etapas 4 a 6 repetem por incremento. Nada vai a produção sem evals no CI e sem o checklist de privacidade preenchido.

## 3. Pontos de aprovação do Samuel

1. Escopo: o que o agente pode e não pode fazer (etapa 1).
2. Provedor de modelo pago, cota paga ou dado pessoal no prompt (etapas 2 e 3).
3. Todo deploy em produção (etapa 7), como na §3 de [governanca-e-aprovacoes.md](../governanca-e-aprovacoes.md).
4. O teto de custo *no contrato* com o cliente não é tarefa deste repositório (agentes de vendas).

## 4. Itens específicos

- **Harness:** um único lugar decide parada, retry e fallback. Não deixar o modelo escolher sozinho uma ferramenta perigosa (e-mail externo, apagar dado, cobrança) sem regra explícita e, se for o caso, A2.
- **Evals:** pelo menos os caminhos feliz, recusa e erro de ferramenta. O portão roda no CI com cliente falso; medição paga de modelo real, se houver, fica fora do CI e é A2.
- **Custo:** o runbook registra o que foi medido (tokens, chamadas). Sem inventar A/B.
- **Privacidade:** mínimo no prompt; nenhum segredo; nada de dado pessoal em log ou em eval versionado.
- **Híbrido:** se o principal for um sistema web com um assistente, o principal permanece [SaaS](sistema-web-saas.md) e este fluxo entra como módulo — as quatro peças (177, 178, 179, 150) continuam obrigatórias.

## 5. Exemplo

"Assistente que preenche um rascunho de laudo a partir do prontuário, para o profissional revisar." Etapa 1: o agente não publica o laudo sozinho. Etapa 2: ADR do laço com no máximo N iterações e ferramentas só de leitura no prontuário. Etapa 3: dado de saúde no prompt é A2. Etapa 4: evals com laudo típico, recusa quando falta dado, e falha da ferramenta. Etapa 7: deploy em produção é A2.

## 6. Checklist de conclusão

- [ ] PRD recorta o que o agente não faz; escopo aprovado
- [ ] ADR do harness (VTX-177) no repositório do cliente
- [ ] Checklist de privacidade (VTX-150) preenchido; dado pessoal tratado como A2
- [ ] Evals no CI (VTX-178) e telemetria de custo (VTX-179) no runbook
- [ ] Deploy em produção com A2
- [ ] Teto contratual, se houver, ficou com os agentes de vendas — não é aceite deste fluxo

## Fontes

- Padrão de funções de domínio para tool-calling: [funcoes-de-dominio.md](../../engenharia/ia/funcoes-de-dominio.md)
- Hospedagem: [hospedagem-por-cliente.md](../../operacao/hospedagem-por-cliente.md) (VTX-195).
- Governança A0–A3: [governanca-e-aprovacoes.md](../governanca-e-aprovacoes.md)
