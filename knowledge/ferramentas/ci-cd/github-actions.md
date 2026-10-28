# GitHub e GitHub Actions
> CI/CD e infraestrutura · Status: **adotado** (repositórios e CI de toda a VTX) · Revisado em 2026-10-28 · VTX-101

## 1. O que é
GitHub guarda o código, os PRs e as revisões; o Actions roda os workflows (`.github/workflows/*.yml`) a cada push, PR ou horário. Aqui fica o **uso prático**; a teoria de branches, pipeline e DORA está em [Git e CI/CD](../../engenharia/git-e-ci-cd.md) (VTX-019).

## 2. Quando usar / quando não usar
- **Usar:** todo repositório da VTX e de cliente (salvo exigência dele); CI em todo PR; tarefas agendadas leves (sincronizar painel, relatórios).
- **Não usar:** processo longo ou servidor permanente (vai para Vercel/Supabase/VPS); runner maior (*larger runner*), que é sempre pago.

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| GitLab CI | cliente usa GitLab | mesma ideia, YAML diferente |
| Runner self-hosted | minutos acabando ou build pesado | grátis em minutos, mas a máquina é nossa (segurança) |
| `act` (local) | testar workflow antes do push | open source, roda no Docker, não gasta minutos |

## 4. Custo e plano gratuito (conferido em 28/10/2026)
- **Conta do Samuel = GitHub Free** (confirmado pela API em 28/10). Repo **público**: Actions grátis sem limite nos runners padrão. Repo **privado**: 2.000 min/mês, 500 MB de artefatos/pacotes e 10 GB de cache por repositório; zera todo mês.
- **Limite do Free em repo privado:** branch protection, rulesets, environments e auto-merge nativo **não existem** (API responde "Upgrade to GitHub Pro"). Por isso o "PR com merge automático no CI verde" da VTX é feito pelo agente: `gh pr checks <n> --watch` e, se verde, `gh pr merge <n> --squash --delete-branch`.
- **Alerta A2:** GitHub Pro/Team, orçamento de Actions acima do grátis ou runner maior são **decisão do Samuel**. Sem orçamento, o Actions só para ao estourar (não cobra).

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | CI e CD | lint, tipos, testes, build; `supabase db push` e deploy |
| [Mobile](../../processos/fluxos/app-mobile.md) | CI | testes e lint; build nativo fica no EAS |
| [API](../../processos/fluxos/api-integracoes.md) | CI | testes de contrato e integração |
| [Site](../../processos/fluxos/site-landing-page.md) | publicação | GitHub Pages direto do Actions |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | segurança | Dependabot, `npm audit`/`pip-audit` semanal |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | CI mínimo | um job de teste, nada além |

## 6. Papel responsável
DevOps escreve e mantém workflows, secrets e environments; Dev Backend/Frontend mantêm os testes verdes; QA define o que bloqueia o merge; Arquiteto revisa permissões; Samuel aprova produção e custo ([papéis](../../../agents/)).

## 7. Setup
1. Copiar o [exemplo mínimo](../../engenharia/git-e-ci-cd.md) para `.github/workflows/ci.yml`; `on: [pull_request, push]` na `main`.
2. Economia: `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }`, filtro `paths`, cache do `setup-node`/`setup-python`, `timeout-minutes: 15`.
3. `permissions: contents: read` no topo; cada job pede só o que usa.
4. Produção: em repo público (ou Pro), job com `environment: production` e segredo no environment; em repo privado no Free, workflow `workflow_dispatch` disparado à mão após o OK do Samuel, com o segredo de produção nos Secrets do repo.
5. Local: `gh run list`, `gh run watch`, `gh pr checks`; `act` para testar antes do push.

## 8. Segredos e segurança/LGPD
- Segredos só em *Secrets* do repositório ou do environment; nunca no YAML, em log (`echo`) ou no chat. Token com escopo mínimo e validade (fine-grained).
- Actions de terceiros fixadas por SHA do commit; as oficiais (`actions/*`) por versão.
- Nunca `pull_request_target` com checkout do código do PR: PR de fork não recebe secrets por padrão, e assim deve ficar.
- Preferir OIDC a chave de nuvem longa quando o destino aceitar. Sem dado pessoal real em teste, fixture ou artefato.

## 9. Checklist
- [ ] CI roda em todo PR e o merge só acontece com ele verde
- [ ] `concurrency`, cache, `paths` e `timeout-minutes` configurados
- [ ] `permissions` mínimas; actions de terceiros por SHA
- [ ] Segredos em Secrets/Environments; nenhum no repositório (gitleaks)
- [ ] Uso de minutos acompanhado (repo privado, 2.000/mês)
- [ ] Deploy de produção só após aprovação do Samuel

## 10. Registro de adoção e Fontes
**ADR curto (28/10/2026):** *Contexto:* todos os repos já estão no GitHub (conta Free). *Opções:* GitHub Actions, GitLab CI, runner próprio. *Decisão:* Actions nos runners padrão, dentro do grátis; merge após CI verde feito pelo agente com `gh`, já que o auto-merge nativo exige Pro em repo privado. *Consequência:* tornar um repo público ou assinar o Pro é decisão do Samuel (A2).
- Cobrança e cota grátis do Actions: https://docs.github.com/en/billing/concepts/product-billing/github-actions
- Auto-merge (disponibilidade por plano): https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository
- Rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- Uso seguro: https://docs.github.com/en/actions/reference/security/secure-use
- Secrets: https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- Environments: https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
- Concorrência: https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency
- Cache: https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching
- OIDC: https://docs.github.com/en/actions/concepts/security/openid-connect
- act: https://github.com/nektos/act
