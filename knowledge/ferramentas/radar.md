# Radar de ferramentas

**Política (aprovada por Samuel em 23/10/2026):** até o piloto começar, ferramentas novas são avaliadas e registradas aqui, **sem** criar tarefa no backlog. Só vira tarefa o que for claramente essencial. Quando o piloto começar, o radar é revisado e os itens "adaptar" viram tarefas priorizadas.

Regras de sempre: só leitura dos repositórios (nunca rodar instaladores, hooks ou scripts deles); nada pago; sem licença = só ideia; copiar MIT/Apache só com atribuição e commit fixo; AGPL = não copiar código para projetos de clientes.

| Data | Repositório (commit lido) | Licença | Telemetria / nuvem / pago | Decisão | O que vira no Cursor |
|---|---|---|---|---|---|
| 24/10/2026 | [volcengine/OpenViking](https://github.com/volcengine/OpenViking) (`4ab22a4`) | AGPL-3.0 | Precisa de provedor de LLM/embeddings (padrão Volcengine/OpenAI); site/estúdio na nuvem ficam de fora | Só ideia | **Processo/conhecimento:** modelo de memória em camadas (resumo curto → visão geral → detalhe) e sessões que viram Markdown, para organizar `knowledge/` e a memória dos agentes. Não instalar; AGPL impede copiar código. |
| 24/10/2026 | [google/artemis](https://github.com/google/artemis) (`351ca84`) | Apache-2.0 | Usa modelo multimodal (Gemini/Claude/GPT ou Qwen-VL local); o `start.sh` instala MCP e regras globais nas IDEs — **não rodar** | Adaptar (quando houver app Expo) | **MCP local** de teste Android para o agente QA (instalação manual e por projeto, nunca global) + **regra** `.cursor/rules` "mentalidade de teste mobile" inspirada no rules.md deles, com atribuição. Entra no fluxo de testes de apps (VTX-018) após o piloto. |
| 24/10/2026 | [pizza-bot-app/pizza-bot](https://github.com/pizza-bot-app/pizza-bot) (`bb9ce39`) — o "Pizza Bot da AWS" (feito na Amazon, projeto comunitário) | Apache-2.0 | Sem telemetria, local-first, aceita Ollama; Bedrock e outros provedores são opcionais/pagos | Só ideia | **Processo:** filas "Não lido" (trabalho pronto) e "Ação" (decisões esperando o Samuel) para o painel e os resumos da VTX; skills como subagentes com ferramentas restritas. Não instalar: a VTX roda dentro do Cursor. |
