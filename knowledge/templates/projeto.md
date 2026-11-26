# Template de repositório de cliente

> VTX-170 · Fase F6. Ponteiro para o template usado pelo bootstrap. Os templates detalhados de PRD, história, ADR, testes, runbook e relatório (VTX-033 a 038) continuam a fazer; aqui entra só o esqueleto.

## Uso

```bash
scripts/bootstrap_projeto.sh [--tipo python|web] <nome> <destino>
# python (padrão): scripts/bootstrap_projeto.sh demo /tmp/demo
# web (Next.js):   scripts/bootstrap_projeto.sh --tipo web demo /tmp/demo
```

- `--tipo python` (padrão) copia [`templates/projeto/`](../../templates/projeto/) e deixa um exemplo `hello` cujo [CI](../../templates/projeto/.github/workflows/ci.yml) roda lint (`compileall`), testes (`unittest`) e build, com `permissions: contents: read`.
- `--tipo web` copia [`templates/web-next/`](../../templates/web-next/) (Next.js, TypeScript, Tailwind, Zod, Vitest, cliente Supabase). O [CI](../../templates/web-next/.github/workflows/ci.yml) roda gitleaks e `npm ci && npm run lint && npm run typecheck && npm test && npm run build`, também com `permissions: contents: read`. O preview comercial fica documentado no runbook (Cloudflare Pages; Vercel Hobby não serve para uso comercial).

## Artefatos

| Caminho no repositório do cliente | Dono |
|---|---|
| `docs/produto/PRD.md` | Produto |
| `docs/arquitetura.md`, `docs/adr/` | Arquiteto |
| `docs/plano.md` | Orquestrador |
| `testes/plano.md` | QA |
| `docs/runbook.md`, `.github/workflows/` | DevOps/SRE |

No vtx-core, os mesmos arquivos ficam dentro de `projects/<proj>/`. Regras do Cursor vêm de [templates/cursor](cursor/README.md).
