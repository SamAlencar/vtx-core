# AGENTS.md — agentes

Orquestração de agente: prompts, tools, harness e memória.

## Pode

- `src/agentes/prompts/`: texto de prompt, nunca regra de negócio.
- `src/agentes/tools/`: schema Zod e chamada a `src/dominio/`.
- `src/agentes/harness/`: único lugar que importa o SDK de modelo.
- `src/agentes/memoria/`: sessão e histórico (a VTX-216 completa).
- `src/agentes/memoria/acoes.ts`: ações pendentes de tool crítica (`critica: true`), aprovadas ou rejeitadas em `app/api/agentes/acoes/[id]/aprovar/` e `.../rejeitar/` (VTX-213). Escrita no banco só no servidor; a leitura autenticada é SELECT por coluna (sem `contexto_retomada`), com a view `acoes_pendentes_leitura` como superfície. O repositório Supabase é `acoes-supabase.ts` (VTX-230), ligado em `acoes-padrao.ts` via service_role; sem a chave, o padrão cai em memória (falha segura). Quem cria a ação (harness/`executarAgente`) precisa usar o mesmo repositório das rotas de aprovar/rejeitar (`repositorioAcoesPadrao` ou a mesma instância injetada); senão a aprovação responde 404.

## Não pode

- Importar o SDK de modelo fora de `src/agentes/harness/`.
- Colocar regra de negócio no prompt ou na tool; a tool delega a `src/dominio/`.
- `src/dominio/` importar esta pasta (veja `src/dominio/AGENTS.md`).

A fronteira é imposta pelo ESLint (`eslint.config.mjs`).

A referência em `/assistente` só responde com `AGENT_MODELO_FALSO=1` (nunca em produção). O provedor real entra em `servicos/exemplo.ts`, com o SDK só neste `harness/`.
