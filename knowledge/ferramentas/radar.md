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

## ponytail (DietrichGebert/ponytail) — avaliado 2026-10-25
- **O que é:** instruções para o agente agir como "o sênior preguiçoso": o melhor código é o que não precisa ser escrito. MIT, ~176k estrelas, commit 09c434a.
- **Uso interno:** vira regra do Cursor para os Devs e o Faxineiro: antes de codar, perguntar se dá para não escrever (reusar, biblioteca, configuração); preferir a menor mudança que resolve. Casa com Pareto e Tesler dos princípios de UX.
- **Decisão:** adaptar como trecho da regra de padrões de código, com atribuição. Não instalar pelo npm.

## i-have-adhd (ayghri/i-have-adhd) — avaliado 2026-10-25
- **O que é:** skill que obriga o agente a pôr a resposta primeiro, curta e escaneável. MIT, ~59k estrelas, commit 1ecea19.
- **Uso interno:** formato padrão dos relatórios dos agentes para o Samuel (resposta na primeira linha, depois detalhes). Reforça as regras de eficiência de tokens.
- **Decisão:** adaptar no template de relatório e na regra de eficiência, com atribuição. Não seguir o "instale pelo prompt" do README.

## superpowers (obra/superpowers) — reavaliado 2026-10-25
- Já está no catálogo (recursos.yaml) e a rotina diária já usa writing-plans e verification-before-completion. MIT, ~305k estrelas, suporta Cursor.
- **Decisão:** manter; avaliar as demais skills (brainstorming, TDD, depuração sistemática) junto com addyosmani/agent-skills quando cada tema chegar no backlog. Ignorar a telemetria do "visual companion".

## OmniRoute (diegosouzapw/omniroute → cheaper-inference/OmniRoute) — avaliado 2026-10-25
- **O que é:** gateway de IA local com um endpoint só para centenas de provedores, troca automática quando a cota acaba e compressão de tokens. MIT, ~81k estrelas, commit 9666fa3. Os tiers grátis exigem contas próprias em cada provedor.
- **Riscos:** juntar contas grátis de vários provedores pode violar os termos de uso de cada um; os dados passam por muitos provedores (LGPD), então nunca dados de clientes. Não usar para trocar o modelo dos agentes do Cursor.
- **Decisão:** ideia. Possível teste depois do piloto só para scripts internos sem dados sensíveis (ex.: simulações tipo MiroFish).

## Strix (usestrix/strix) — avaliado 2026-10-25
- **O que é:** agentes de IA que fazem teste de invasão (pentest): rodam a aplicação, acham falhas e as comprovam com prova de conceito. Apache-2.0, ~72k estrelas, commit 200a501. Precisa de chave de LLM e Docker.
- **Uso interno:** atende a competência 8 (segurança). Rodar localmente contra o ambiente de teste antes de cada go-live (primeiro: plataforma-projetos).
- **Regras:** só contra sistemas próprios ou de cliente com autorização escrita; nunca produção; não usar o serviço hospedado app.strix.ai; revisar o código e rodar dentro de contêiner isolado.
- **Decisão:** adaptar, no checklist de go-live do fluxo de segurança.

## Open WebUI (open-webui/open-webui) — avaliado 2026-10-25 para a plataforma-projetos
- **O que é:** interface de chat de IA self-hosted, com Ollama e APIs compatíveis com OpenAI, RAG e plugins. ~157k estrelas. Licença própria (BSD + cláusula de marca).
- **Limite da licença:** acima de 50 usuários finais em 30 dias, é proibido tirar ou trocar a marca "Open WebUI" sem licença enterprise paga.
- **Decisão:** não usar como base da plataforma-projetos (produto com marca Tekto e mais de 50 usuários, e ela é um fluxo de projeto e revisão, não um chat genérico). A interface de IA da plataforma usa o stack (Next.js + Vercel AI SDK + thinking-orbs). Uso interno ok: chat com modelos locais para a equipe Tekto/VTX, com menos de 50 usuários. Ideias para copiar como conceito: biblioteca de documentos com RAG, seleção de modelo, histórico.

## Plandex (plandex-ai/plandex) — avaliado 2026-10-26
- **O que é:** agente de código no terminal (Go, MIT, ~16k estrelas) para tarefas longas em muitos arquivos: contexto de até 2M tokens, mapa do projeto com tree-sitter, sandbox de diffs acumulados antes de aplicar, versões e branches do plano.
- **Situação:** sem commits desde 03/10/2025; o Plandex Cloud foi encerrado. Só modo local com Docker e chaves de API próprias (pagas).
- **Uso interno:** não substitui o Cursor e duplicaria custo de modelo. Ideias já cobertas pela VTX: plano antes de executar (writing-plans) e mudanças isoladas até revisão (PR com CI verde). Ideia a aproveitar: testar duas abordagens em branches paralelas e comparar antes de escolher, em decisões de arquitetura.
- **Decisão:** ideia apenas; projeto parado, não instalar.
