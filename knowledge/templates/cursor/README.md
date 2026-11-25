# Regras do Cursor (padrão VTX)

Base criada pelo Samuel em 20/10/2026. Todo repositório de projeto da VTX recebe na raiz:
- `.cursorignore` → raiz do repo.
- `eficiencia-de-tokens.mdc` → `.cursor/rules/` (formato atual do Cursor; o `.cursorrules` na raiz é legado, mas o conteúdo é o mesmo).

Adaptações feitas pelo Sys (conservadoras): modo autônomo para as regras que pedem "pergunte/aguarde Ok"; `*.svg` liberado em projetos web; `.next/` incluído; exceção `!arquivo` para CSV/PDF que sejam insumo. Já aplicado no próprio vtx-core.

Em cada repositório de projeto também entram, sob demanda (não always-on):
- `docs/CODEBASE_MAP.md` — [mapa de codebase](../../engenharia/mapa-de-codebase.md).
- `docs/memoria/` — [memory bank](../memoria-projeto/README.md); o ponteiro vai no `AGENTS.md` ou numa regra curta.
- `economia-de-contexto.mdc` → `.cursor/rules/` (sob demanda, `alwaysApply: false`) — filtrar logs, rg em vez de ler arquivo, resumir JSON e diffs (VTX-133).

O repositório de cliente gerado pelo [template de projeto](../projeto.md) (`scripts/bootstrap_projeto.sh`) já recebe essas regras em `.cursor/rules/`.
