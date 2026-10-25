# Radar de ferramentas

**Princípio (Samuel, 24/10/2026):** os repositórios avaliados aqui são para **uso interno da VTX** (agentes e operação no Cursor), não para replicar em projetos de clientes. Restrições de licença (AGPL, GPL, source-available) só pesam se o código for **copiado para entregas de clientes** ou distribuído; rodar localmente na VTX é permitido. Código **sem licença** continua sem permissão de cópia nem de uso (só ideia).

**Política (aprovada por Samuel em 23/10/2026):** até o piloto começar, ferramentas novas são avaliadas e registradas aqui, **sem** criar tarefa no backlog. Só vira tarefa o que for claramente essencial. Quando o piloto começar, o radar é revisado e os itens "adaptar" viram tarefas priorizadas.

Regras de sempre: só leitura dos repositórios (nunca rodar instaladores, hooks ou scripts deles); nada pago; sem licença = só ideia; copiar MIT/Apache só com atribuição e commit fixo; AGPL/GPL: uso interno ok; não copiar para entregas de clientes.

| Data | Repositório (commit lido) | Licença | Telemetria / nuvem / pago | Decisão | O que vira no Cursor |
|---|---|---|---|---|---|
| 24/10/2026 | [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | AGPL-3.0 (uso interno ok) | Suporta **Ollama local** para modelo e embeddings (também Volcengine/OpenAI, pagos — não usar); site/estúdio na nuvem ficam de fora | Adaptar (uso interno, teste após o piloto) | **MCP local** de memória/contexto dos agentes da VTX, com Ollama e dados só no computador; espelha `knowledge/` em camadas (resumo → visão geral → detalhe). Sem instalador deles: instalação manual revisada via script TT-060. Risco: qualidade de embeddings locais; se não ficar melhor que a busca atual (rg + INDEX), descarta. |
| 24/10/2026 | [google/artemis](https://github.com/google/artemis) | Apache-2.0 | Precisa de modelo multimodal (Qwen-VL local via Ollama é gratuito) e de celular/emulador Android; o `start.sh` instala MCP e regras globais — **não rodar** | Adaptar (só quando a VTX tiver app Android para testar) | **MCP local** do agente QA da VTX + **regra** `.cursor/rules` de mentalidade de teste mobile (com atribuição). Hoje não tem uso: não há app; os sites usam Playwright. |
| 24/10/2026 | [pizza-bot-app/pizza-bot](https://github.com/pizza-bot-app/pizza-bot) — o "Pizza Bot da AWS" (feito na Amazon, projeto comunitário) | Apache-2.0 | Sem telemetria, local-first, aceita Ollama; Bedrock/Anthropic/OpenAI são pagos — não usar | Só ideia por enquanto | Poderia ser o executor/caixa de entrada dos agentes da VTX, mas os agentes rodam no Cursor (modelos do Cursor) e com Ollama a qualidade cai; seria um segundo executor paralelo. Aproveitar o **processo**: filas "Não lido" e "Ação" no painel e nos resumos. Reavaliar se a VTX precisar de agentes fora do Cursor. |

## MiroFish (666ghj/MiroFish) — avaliado 2026-10-24
- **O que é:** motor de simulação com vários agentes de IA. A partir de documentos, monta um grafo de conhecimento, cria agentes com personas e memória, simula a interação entre eles e gera um relatório de "previsão". AGPL-3.0, ~81k estrelas. Há um fork offline com Neo4j e Ollama (nikmcfly/MiroFish-Offline).
- **Uso interno possível:** simular como personas (clientes, profissionais revisores) reagem a um PRD, preço ou funcionalidade antes de construir. A AGPL não atrapalha no uso interno.
- **Limites:** gasta muitos tokens de LLM; as previsões não são validadas, então servem só como indício e nunca substituem a entrevista ou o teste com usuários reais. A versão original usa o Zep, que é pago; só o fork offline é aceitável.
- **Decisão:** ideia, com teste opcional depois do piloto, usando o fork offline com Ollama. Não roda instaladores nem scripts sem revisar.

## thinking-orbs (jakubantalik/thinking-orbs) — avaliado 2026-10-24
- **O que é:** indicadores de carregamento animados (orbes pontilhados) para interfaces de IA e agentes. 9 tipos, dois tamanhos, tema claro/escuro automático. TypeScript, MIT, commit de85557. Demo: orbs.jakubantalik.com.
- **Uso:** estado "pensando" quando a IA trabalha, como na plataforma-projetos enquanto a Tekto gera um projeto e no painel da VTX quando houver ações em andamento. Também ajuda o Pico-Fim dos princípios de UX: a espera parece viva.
- **Licença:** MIT permite uso também em projetos de clientes, com atribuição e commit fixado.
- **Decisão:** adotar como componente de referência do stack (Next.js/Tailwind) quando a primeira tela de IA for construída. Ler o código antes; não rodar scripts de instalação sem revisar.

## agent-skills (addyosmani/agent-skills) — avaliado 2026-10-24
- **O que é:** 24 skills de engenharia para agentes de código (API design, TDD, code review, debugging, CI/CD, segurança, performance, ADRs, spec-driven, planejamento, lançamento, interview-me...) + pasta evals/ com casos de teste das skills. MIT, ~110k estrelas, commit aeac41d.
- **Uso interno:** referência direta para as próximas tarefas de conhecimento (VTX-024 Design de APIs usa api-and-interface-design) e para as skills em .cursor/skills/. O padrão de evals serve à manutenção quinzenal de skills do Vix.
- **Licença:** MIT; copiar trechos com atribuição e commit fixado. Revisar como biblioteca (regra de skills da comunidade); não rodar scripts.
- **Decisão:** adaptar. Consultar a skill correspondente antes de escrever cada documento ou skill da VTX; adotar o formato de evals.

## billion-context (ranxianglei/billion-context) — avaliado 2026-10-25
- **O que é:** plugin de compressão de contexto para sessões muito longas. O próprio modelo decide quando e o que comprimir (compress, decompress, search_context), e o autor diz que basta uma janela de 100k tokens e que o gasto cai cerca de 5 vezes. Funciona nos harnesses pi, opencode e DeepSeek, não no Cursor. Licença "Other" (não padrão); os forks são MIT. ~2,8k estrelas.
- **Uso interno:** não pluga no Cursor, que tem gerenciamento de contexto próprio. A ideia aproveitável: ao fim de cada tarefa, o agente grava um resumo compacto e pesquisável (decisões, arquivos tocados, pendências) em vez de reler histórico, reforçando as regras de eficiência de tokens.
- **Decisão:** ideia apenas. Licença não padrão, então nenhum código é copiado.
