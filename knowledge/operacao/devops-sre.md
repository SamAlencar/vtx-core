# DevOps e SRE (IaC, SLOs, incidentes)

> VTX-021 · Fase F3 · Base de Conhecimento. O que o **DevOps/SRE** ([devops-sre.md](../../agents/devops-sre.md)) mantém depois do merge. Continua [Git e CI/CD](../engenharia/git-e-ci-cd.md) (pipeline e DORA) e se apoia em [segurança](../seguranca/desenvolvimento-seguro.md). Observabilidade detalhada: [observabilidade.md](observabilidade.md) (VTX-022). SLA de suporte ao cliente (tempos de resposta, horas, canal e monitor): [suporte-e-sla.md](suporte-e-sla.md) (VTX-199).

## 1. Conceitos
- **Infraestrutura como código (IaC):** todo ambiente é descrito em arquivo versionado e revisado por PR; nada é configurado "na mão" no painel sem virar código ou runbook.
- **SLI / SLO / error budget:** SLI é a medida (ex.: % de requisições com sucesso em < 500 ms); SLO é a meta (ex.: 99,5 % em 28 dias); o *error budget* é o que sobra (0,5 % ≈ 3,4 h/28 dias) e decide entre lançar ou estabilizar.
- **Toil:** trabalho manual repetitivo; vira script no arsenal quando se repete 3 vezes.
- **Postmortem sem culpados:** foco em causa sistêmica e ação corretiva, não em quem errou.

## 2. Ambientes e IaC no stack VTX (planos grátis)
| Ambiente | Onde | Como é criado | Deploy |
|---|---|---|---|
| dev | máquina local | `supabase start` (Docker) + `.env.local` | — |
| homologação | Vercel *preview* + projeto Supabase de teste | merge na `main` | automático + *smoke test* |
| produção | Vercel *production* + Supabase produção | tag `v*` | **aprovação de Samuel** + rollback pronto |

- Banco: só por **migração versionada** (`supabase/migrations/`, `supabase db push`); nunca alterar esquema pelo painel. Migração destrutiva (DROP, renomear coluna) em dois passos: expandir → migrar dados → contrair.
- Configuração de plataforma: `vercel.json`, variáveis por ambiente; recursos de nuvem, se surgirem, em [OpenTofu](https://opentofu.org/) (open source) com `plan` revisado no PR.
- Segredos: GitHub Environments / variáveis da Vercel e Supabase; rotação é decisão do Samuel.
- **Custo:** qualquer passagem de plano grátis para pago escala ao Samuel antes ([governança](../processos/governanca-e-aprovacoes.md)).

## 3. SLOs padrão VTX (ajustados por projeto no PRD)
| Serviço | SLI | SLO inicial (28 dias) |
|---|---|---|
| API/site | requisições não-5xx | 99,5 % |
| API | latência p95 | < 500 ms |
| Jobs/fila | processados sem erro em < 15 min | 99 % |

**Política de error budget:** consumo > 50 % na janela → só correções e confiabilidade até recuperar; budget esgotado → congelar novas funcionalidades e abrir ação no backlog.

## 4. Incidentes
| Sev | Exemplo | Resposta | Avisar Samuel |
|---|---|---|---|
| SEV1 | produção fora / vazamento de dados | imediata; rollback primeiro, investigar depois | na hora |
| SEV2 | funcionalidade principal degradada | ≤ 1 h | no mesmo dia |
| SEV3 | defeito com contorno | próximo ciclo | relatório semanal |

Fluxo: detectar (alerta) → declarar severidade e um responsável → mitigar (rollback na Vercel, *feature flag* desligada, migração de reversão) → comunicar → **postmortem em até 5 dias úteis** para SEV1/2 em `docs/postmortems/AAAA-MM-DD-titulo.md` (linha do tempo, impacto, causa, o que ajudou, ações com dono e prazo).

## 5. Runbook mínimo por projeto (`docs/runbook.md`)
Como fazer deploy e rollback · como restaurar backup do banco (testado 1×/trimestre) · onde ver logs e alertas · contatos e limites de escalonamento · SLOs vigentes.

## 6. Checklist
- [ ] Ambientes dev/homologação/produção separados; produção só por tag com aprovação.
- [ ] Esquema do banco 100 % em migrações; migração destrutiva em dois passos.
- [ ] Rollback testado antes do primeiro deploy em produção.
- [ ] SLOs definidos no PRD e painel de acompanhamento ativo.
- [ ] Alertas acionáveis (cada alerta tem runbook); sem alerta de "ruído".
- [ ] Backup e restauração testados; segredos fora do código.
- [ ] Postmortem sem culpados para SEV1/2, com ações no backlog.

## 7. Fontes
- Google, [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) (caps. SLOs, Eliminating Toil, Postmortem Culture) · [The SRE Workbook — Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [DORA — capacidades](https://dora.dev/capabilities/) · [OpenTofu](https://opentofu.org/docs/)
- [Supabase — migrações locais](https://supabase.com/docs/guides/deployment/database-migrations) · [Vercel — rollback](https://vercel.com/docs/instant-rollback)
- PagerDuty, [Incident Response Guide](https://response.pagerduty.com/) (guia aberto, ferramenta não adotada)
