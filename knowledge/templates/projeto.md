# Template de repositório de cliente

> VTX-170 · Fase F6. Ponteiro para o template usado pelo bootstrap. Os templates detalhados de PRD, história, ADR, testes, runbook e relatório (VTX-033 a 038) continuam a fazer; aqui entra só o esqueleto.

## Uso

```bash
scripts/bootstrap_projeto.sh <nome> <destino>
# exemplo: scripts/bootstrap_projeto.sh demo /tmp/demo
```

O script copia [`templates/projeto/`](../../templates/projeto/), troca `__NOME_DO_PROJETO__` e deixa um exemplo `hello` cujo [`.github/workflows/ci.yml`](../../templates/projeto/.github/workflows/ci.yml) roda lint (`compileall`), testes (`unittest`) e build.

## Artefatos

| Caminho no repositório do cliente | Dono |
|---|---|
| `docs/produto/PRD.md` | Produto |
| `docs/arquitetura.md`, `docs/adr/` | Arquiteto |
| `docs/plano.md` | Orquestrador |
| `testes/plano.md` | QA |
| `docs/runbook.md`, `.github/workflows/` | DevOps/SRE |

No vtx-core, os mesmos arquivos ficam dentro de `projects/<proj>/`. Regras do Cursor vêm de [templates/cursor](cursor/README.md).
