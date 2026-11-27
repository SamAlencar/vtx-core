# AGENTS.md — domínio

Esta pasta é a regra de negócio. Não conhece HTTP, tela, prompt nem modelo.

## Pode

- Funções e tipos puros, schemas Zod de regra, erros de domínio.
- Importar `lib/` só quando for utilitário sem SDK de modelo (por exemplo `lib/http/problema.ts`).

## Não pode

- Importar `src/agentes/` (prompts, tools, harness, memória).
- Importar o SDK de modelo (`ai`, `@ai-sdk/*`).
- Fazer I/O de rede ou ler `process.env` de serviço.

Quem chama o domínio é a API, a tool ou o teste — não o contrário. A fronteira é imposta pelo ESLint (`eslint.config.mjs`).
