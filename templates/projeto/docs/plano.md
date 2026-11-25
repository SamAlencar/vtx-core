# Plano — __NOME_DO_PROJETO__

Plano do incremento (Orquestrador). Uma tarefa = um PR.

## Objetivo do incremento

## Tarefas

| ID | Título | Dono | Depende de | Status |
|---|---|---|---|---|
| | | | | |

## Impedimentos e aprovações (A2)

## Notas de handoff

## CI do template hello

O workflow [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) roda com `permissions: contents: read`.
Os passos Lint e Build do exemplo `hello` usam o mesmo `python -m compileall`: o Build é **provisório** até o projeto ter um passo real (bundle, wheel ou equivalente).
