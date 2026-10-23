# Git e CI/CD

> VTX-019 · Fase F2 · Base de Conhecimento. O que o **DevOps/SRE** ([devops-sre.md](../../agents/devops-sre.md)) mantém e o que todo agente segue ao versionar. Complementa [padrões de código](padroes-de-codigo.md) (PR e commits) e [testes](testes-e-qualidade.md) (o que a CI roda).

## 1. Fluxo de branches: trunk-based com PR curto
- `main` sempre implantável e **protegida** (sem push direto, PR com 1 aprovação de agente ≠ autor, CI obrigatória).
- Branch por issue, vida < 2 dias: `feat/HU-07-imposto`, `fix/123-login`, `docs/...`.
- Merge **squash** com título em [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/); funcionalidade incompleta entra atrás de *feature flag*, não em branch longa ([trunk-based](https://trunkbaseddevelopment.com/)).
- **Proibido:** `--force` em branch compartilhada, `--no-verify`, commitar `.env` ou segredo (regras que o VTX-139 transforma em hooks).
- Versão: [SemVer](https://semver.org/lang/pt-BR/) + tag `vX.Y.Z` e CHANGELOG gerado dos commits.

## 2. Pipeline (GitHub Actions, cota grátis)
| Etapa | Quando | O que roda | Bloqueia? |
|---|---|---|---|
| 1. Pre-commit (local) | cada commit | formatador, linter, [gitleaks](https://github.com/gitleaks/gitleaks) | sim |
| 2. CI | todo PR e `main` | instalar com cache → lint → tipos → unidade → integração → build | sim |
| 3. E2E | PR para `main` | Playwright contra build local | sim |
| 4. Segurança | PR + semanal | `npm audit`/`pip-audit`, [Dependabot](https://docs.github.com/pt/code-security/dependabot), [CodeQL](https://codeql.github.com/) (grátis em repo público) | crítico sim |
| 5. CD homologação | merge na `main` | deploy automático + *smoke test* | — |
| 6. CD produção | tag `v*` | deploy com **aprovação humana** (environment protegido) + rollback pronto | — |

Economia de minutos: `concurrency` cancela execuções antigas, cache de dependências, filtro `paths`, nada de runner pago. Segredos só em *GitHub Secrets/Environments*, nunca no YAML ([governança](../processos/governanca-e-aprovacoes.md): deploy em produção é ação aprovada por Samuel).

## 3. Exemplo mínimo (`.github/workflows/ci.yml`)
```yaml
name: ci
on: { pull_request: {}, push: { branches: [main] } }
concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }
permissions: { contents: read }
jobs:
  testes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run lint && npm run typecheck
      - run: npm test -- --coverage
      - run: npm run build
```
Referência interna: o próprio vtx-core usa `testes.yml` (unittest) e `sincronizar-painel.yml` (publica o painel quando `backlog/` muda).

## 4. Métricas (DORA)
Frequência de deploy, tempo de mudança (commit → produção), taxa de falha de mudança e tempo de recuperação. Meta inicial VTX: deploy em homologação diário, PR aberto < 1 dia, falha de mudança < 15 % ([DORA](https://dora.dev/guides/dora-metrics-four-keys/)).

## 5. Checklist
- [ ] `main` protegida; CI obrigatória; revisor ≠ autor.
- [ ] Branch curta com nome da issue; squash com Conventional Commit.
- [ ] Pre-commit com formatador, linter e gitleaks; sem `--no-verify` nem force-push.
- [ ] CI com cache, `concurrency` e `permissions` mínimas; segredos só em Secrets.
- [ ] Produção só por tag, com aprovação humana e rollback testado.

## 6. Fontes
- [Trunk Based Development](https://trunkbaseddevelopment.com/) · Fowler, [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)
- [GitHub Actions — documentação](https://docs.github.com/pt/actions) · [Uso seguro (security hardening)](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- [DORA metrics](https://dora.dev/guides/dora-metrics-four-keys/) · [SemVer](https://semver.org/lang/pt-BR/) · [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/)
