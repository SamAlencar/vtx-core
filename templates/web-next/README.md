# __NOME_DO_PROJETO__

Repositório de cliente da VTX, gerado por `scripts/bootstrap_projeto.sh --tipo web`.

## Começar

1. Leia o [AGENTS.md](AGENTS.md).
2. `npm ci` e `npm run dev`.
3. Preencha o [PRD](docs/produto/PRD.md) e o [plano](docs/plano.md).
4. Copie [`.env.example`](.env.example) para `.env` (não commite o `.env`).
5. O CI em [`.github/workflows/ci.yml`](.github/workflows/ci.yml) roda gitleaks, `lint`, `typecheck`, `test` e `build`, com `permissions: contents: read`.

## Scripts

```bash
npm ci
npm run lint
npm run typecheck
npm test
npm run build
npm run evals
```

`npm test` é o Vitest (unitário). `npm run evals` é o portão da suíte de agentes (respostas gravadas, sem rede). O Playwright (`npm run test:e2e`) é opcional e o CI ainda não o exige no caminho mínimo (VTX-217).

## Estrutura

- `app/` — App Router (Next.js)
- `lib/env.ts` — variáveis públicas validadas com Zod
- `lib/supabase.ts` — cliente Supabase só quando as env existem
- `docs/produto/PRD.md`, `docs/arquitetura.md`, `docs/adr/`, `docs/plano.md`, `testes/plano.md`, `docs/runbook.md`
- Preview e hospedagem: [docs/runbook.md](docs/runbook.md)

## Assistente de referência

A tela [`/assistente`](app/assistente/page.tsx) e o `POST /api/agentes/exemplo` só respondem com o modelo falso, ligando `AGENT_MODELO_FALSO=1` no `.env` (desenvolvimento, testes e e2e). Sem o flag, a rota devolve 500. Não use o flag em produção: com `NODE_ENV=production` ele é recusado.

Para um provedor real, implemente a obtenção do modelo em `src/agentes/servicos/exemplo.ts` (`modeloPadrao`), instanciando o SDK só em `src/agentes/harness/`, com a chave só no servidor (veja [`.env.example`](.env.example)). Ligar um provedor real é A2.

## Isolamento e segredos

Este é o repositório do cliente: código, dados e *GitHub Secrets* ficam aqui, não no vtx-core. Use `.env` local e nunca o commite. Política: no vtx-core, `knowledge/seguranca/isolamento-clientes.md`.
