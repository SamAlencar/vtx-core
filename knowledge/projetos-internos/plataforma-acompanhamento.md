# Projeto interno: plataforma de acompanhamento da VTX

> VTX-085 · Fase F11 · Projeto interno. Plano da plataforma em que o Samuel acompanha projetos, tarefas e o fluxo entre agentes. O código fica no repositório privado `SamAlencar/vtx-acompanhamento` (nome provisório, pode ser renomeado). **A fonte da verdade continua no `vtx-core`** (backlog, base de conhecimento, agentes), e a plataforma só lê e apresenta. Segue o [fluxo de MVP / prova de conceito](../processos/fluxos/mvp-poc.md).

## 1. Objetivos
1. Mostrar em uma tela **onde está cada projeto** e o que está travado.
2. Mostrar **o que cada agente fez e para quem passou** (handoffs do [SOP](../processos/fluxo-entre-agentes.md)).
3. Concentrar **o que depende do Samuel** em uma fila única de aprovações (portões dos fluxos).
4. Registrar **decisões** tomadas pelos agentes ("decidir o mínimo, documentar sempre").
5. Medir **ritmo, qualidade e custo** (incluindo cota de tokens e saldo do Cursor) e **alertar** antes do problema.

Fora do objetivo: substituir o GitHub ou o backlog YAML, ou criar um gestor de tarefas próprio.

## 2. Usuários
| Usuário | Uso | Permissão |
|---|---|---|
| Samuel (dono/aprovador) | Visão geral, fila de aprovações, decisões, custos | Leitura total; aprova pelo GitHub (PR/issue) |
| Orquestrador | Atualiza status, registra handoffs, gera alertas | Escreve só no `vtx-core` (YAML) |
| Demais papéis ([agents/](../../agents/README.md)) | Registram eventos e decisões do próprio trabalho | Escrevem via YAML/PR |
| Público | Continua vendo só o [painel público](https://samalencar.github.io/vtx_painel/) sanitizado | Sem acesso à plataforma |

## 3. Funcionalidades
| # | Funcionalidade | Conteúdo | MVP? |
|---|---|---|---|
| 1 | Portfólio | Projetos (vtx-core, plataforma-projetos, projetos em `projects/`), tipo da triagem, fase, % concluído, próxima tarefa, bloqueios | Sim |
| 2 | Backlog e fases | Status efetivo por fase, dependências (`depende_de`), tarefas paradas | Sim |
| 3 | Atividade dos agentes | Linha do tempo por papel: tarefa, artefato, handoff (de → para), devoluções e retrabalho | Sim |
| 4 | Fila de aprovações | Portões pendentes do Samuel (fluxos, `mvp-poc` §3, SOP §5), com prazo e link para aprovar | Sim |
| 5 | Registro de decisões | Decisão, quem decidiu, motivo, se é reversível, link; filtro "escalado x decidido pelo agente" | Sim |
| 6 | Métricas | Vazão (tarefas/semana), lead time, retrabalho, CI verde/vermelha, progresso por fase | Parcial |
| 7 | Custos e tokens | Cota semanal Grok Bot (%), saldo sob demanda do Cursor, serviços pagos ativos | Parcial (registro manual) |
| 8 | Alertas | Tarefa parada > 1 dia, aprovação vencida, CI falhando, cota > 80%, rotina que não rodou | Sim (no resumo diário) |
| 9 | Interface web interativa | Filtros, gráficos, celular | Depois |
| 10 | Ações pela plataforma | Aprovar/recusar direto na tela | Depois (via GitHub) |

## 4. Fontes de dados
| Dado | Fonte (verdade) | Situação |
|---|---|---|
| Projeto, fases, tarefas, status | `backlog/projeto.yaml` + diários ([SCHEMA](../../backlog/SCHEMA.md)), via `scripts/backlog_lib.py` | Existe |
| Eventos e handoffs | Novo `registro/eventos/AAAA-MM-DD.yaml` (VTX-087) + issues/PRs do GitHub | A criar |
| Decisões | Novo `registro/decisoes.yaml` (VTX-087) | A criar |
| Aprovações | Novo `registro/aprovacoes.yaml` + issues com rótulo `aprovacao-samuel` (alinhado à VTX-064) | A criar |
| CI e commits | API do GitHub (workflows `testes` e `sincronizar-painel`) | Existe |
| Custos/tokens | Novo `registro/custos.yaml`, preenchido pelos agentes quando há aviso de cota/saldo | A criar (sem API) |
| Projetos de cliente | `projects/<p>/ficha.yaml` (triagem) e repositórios de projeto | Parcial |

Regra: todo formato novo é documentado no `SCHEMA.md`, validado no CI (`tests/`) e marcado campo a campo como PÚBLICO/PRIVADO, como o backlog atual.

## 5. Arquitetura
| Opção | Prós | Contras |
|---|---|---|
| A. Ampliar o `vtx_painel` público | Já existe | Público: **não pode** mostrar decisões, custos e handoffs |
| B. **Painel privado em Markdown** gerado pelo CI no repositório privado | Custo zero, privacidade pelo login do GitHub, abre no app do GitHub no celular, reaproveita `backlog_lib.py` | Pouca interatividade |
| C. Site estático (HTML/JS) com controle de acesso (ex.: Cloudflare Pages + Access) | Interativo, gratuito no início | Serviço externo novo, configuração de acesso = decisão do Samuel |
| D. Aplicação com backend e banco | Ações e tempo real | Caro e complexo para o momento |

Observação: GitHub Pages publica o site em modo público mesmo quando o repositório é privado (o modo privado exige Enterprise), então ele não serve para a plataforma.

**Recomendação conservadora:** começar pela **B**, em etapas:
1. **MVP (B):** workflow agendado no `vtx-acompanhamento` faz checkout do `vtx-core` (token só de leitura), gera `dados/plataforma.json` e páginas `painel/*.md` (portfólio, fases, agentes, aprovações, decisões, métricas). O `vtx_painel` público continua igual.
2. **Evolução (C):** a mesma `plataforma.json` alimenta uma interface web estática com acesso restrito. Só depois de avaliar o MVP e de o Samuel aprovar o serviço (ADR na VTX-095).
3. **Ações:** aprovações continuam no GitHub (review de PR, comentário em issue). Sem backend próprio até haver necessidade comprovada (D fica descartada por enquanto).

## 6. Segurança
- Nada sensível no `vtx_painel` público. Decisões, custos, notas e responsáveis só no repositório privado.
- Token de leitura com escopo mínimo (somente os repositórios lidos), guardado em secret do GitHub e nunca colado em chat.
- Sem dados pessoais de clientes no JSON. Projetos de cliente aparecem por código/apelido (LGPD).
- O gerador nunca escreve no `vtx-core`: o fluxo é só de leitura.

## 7. Escopo do MVP x depois
- **MVP (VTX-086 a VTX-094):** portfólio, fases, atividade/handoffs, fila de aprovações, decisões, métricas básicas, custos registrados à mão, alertas no resumo diário. Tudo em Markdown privado.
- **Depois (VTX-095 a VTX-097):** interface web com acesso restrito, inclusão de projetos de cliente e de outros repositórios, gráficos históricos.

## 8. Como segue os fluxos da VTX
| Etapa do `mvp-poc` | Na plataforma |
|---|---|
| 0 Triagem | Projeto interno, `tipo_principal: mvp-poc` (evoluindo para `sistema-web-saas` na etapa C) |
| 1 Descoberta | Este documento (dono = Samuel; necessidades já conhecidas pelo chat) |
| 2 Hipóteses (**portão Samuel**) | VTX-086. Ex.: "com o painel privado, o Samuel acompanha tudo em ≤ 5 min/dia e só abre o chat para aprovar" |
| 3 Experimento | VTX-087 a VTX-089: formatos e dados, opção B, apetite de ~2 semanas |
| 4 Construção | VTX-090 a VTX-093, uma tarefa por dia, CI verde antes de merge |
| 5 a 6 Medição e decisão (**portão Samuel**) | VTX-094: uso real por 1 semana e decisão continuar/pivotar/parar |
| 7 Transição | VTX-095 (ADR da interface web) e seguintes |

Papéis: Orquestrador (dono do fluxo e dos registros), Produto (PRD e hipóteses), Arquiteto (formatos e ADR), Dev Backend (gerador), Dev Frontend (páginas e, depois, interface web), QA (testes do gerador e da sanitização), DevOps/SRE (workflows, token, agendamento).

## 9. Plano conjunto com a base de conhecimento
- Formatos novos (`registro/`) nascem no `vtx-core` e no `SCHEMA.md`, nunca só na plataforma.
- A plataforma é o primeiro **consumidor** de VTX-014 (governança), VTX-038 (relatórios), VTX-063 e VTX-064 (orquestração e aprovações) e VTX-073 (validação no CI). Quando essas tarefas forem feitas, devem citar os formatos daqui.
- Lições do MVP voltam para a base na retrospectiva (como na VTX-052).

## 10. Posição no backlog
Fase **F11** entre F9 (integração com o Cursor) e F8 (consolidação e piloto), prioridades 67 a 79. F8 e F10 passaram a 80 a 96, sem mudança na ordem relativa entre elas. Motivos: a atividade dos agentes depende das convenções de issues/PRs da F9 (VTX-063/064), e o piloto (F8) ganha com a plataforma pronta para ser acompanhado. Se F9 for antecipada (decisão do resumo semanal de 16/10), F11 continua logo depois dela.

## Checklist
- [x] Objetivos, usuários, funcionalidades, fontes, arquitetura, segurança, MVP
- [x] Fase F11 no backlog com tarefas pequenas
- [ ] Hipóteses aprovadas pelo Samuel (VTX-086)
- [ ] ADR da interface web aprovado (VTX-095)

## Fontes
- Base VTX: [SOP entre agentes](../processos/fluxo-entre-agentes.md), [MVP/PoC](../processos/fluxos/mvp-poc.md), [triagem](../processos/fluxos/triagem.md), [SCHEMA](../../backlog/SCHEMA.md).
- GitHub Docs: "About GitHub Pages" (visibilidade de sites de repositórios privados); "Managing your personal access tokens" (tokens de escopo fino).
- Forsgren, Humble e Kim, *Accelerate* (métricas de vazão e lead time).
