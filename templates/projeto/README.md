# __NOME_DO_PROJETO__

Repositório de cliente da VTX, gerado por `scripts/bootstrap_projeto.sh`.

## Começar

1. Leia o [AGENTS.md](AGENTS.md).
2. Preencha o [PRD](docs/produto/PRD.md) e o [plano](docs/plano.md).
3. O CI em [`.github/workflows/ci.yml`](.github/workflows/ci.yml) roda lint, testes e build do exemplo `hello`.

## Estrutura

- `docs/produto/PRD.md` — requisitos (Produto)
- `docs/arquitetura.md` e `docs/adr/` — arquitetura e decisões (Arquiteto)
- `docs/plano.md` — plano do incremento (Orquestrador)
- `testes/plano.md` — plano de testes (QA)
- `docs/runbook.md` — operação e rollback (DevOps/SRE)
- `src/hello.py` e `tests/test_hello.py` — exemplo inicial (substitua pelo código do projeto)
- `.env.example` — variáveis de ambiente; copie para `.env` e não commite o `.env`
