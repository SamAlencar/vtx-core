# AGENTS.md — agentes

Orquestração de agente: prompts, tools, harness e memória.

## Pode

- `src/agentes/prompts/`: texto de prompt, nunca regra de negócio.
- `src/agentes/tools/`: schema Zod e chamada a `src/dominio/`.
- `src/agentes/harness/`: único lugar que importa o SDK de modelo.
- `src/agentes/memoria/`: sessão e histórico (a VTX-216 completa).

## Não pode

- Importar o SDK de modelo fora de `src/agentes/harness/`.
- Colocar regra de negócio no prompt ou na tool; a tool delega a `src/dominio/`.
- `src/dominio/` importar esta pasta (veja `src/dominio/AGENTS.md`).

A fronteira é imposta pelo ESLint (`eslint.config.mjs`).

A referência em `/assistente` só responde com `AGENT_MODELO_FALSO=1` (nunca em produção). O provedor real entra em `servicos/exemplo.ts`, com o SDK só neste `harness/`.
