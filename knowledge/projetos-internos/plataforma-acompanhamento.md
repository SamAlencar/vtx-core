# Projeto interno: plataforma de acompanhamento da VTX

> VTX-085/VTX-114 · Fase F11 · Projeto interno · v2 (2026-10-17). A plataforma é o ambiente em que o Samuel acompanha projetos, agentes, ferramentas e conexões. O código fica no repositório privado `SamAlencar/vtx-acompanhamento` (nome provisório). **A fonte da verdade continua no `vtx-core`.** O projeto segue o [fluxo de MVP / prova de conceito](../processos/fluxos/mvp-poc.md) e usa o [catálogo de ferramentas](../ferramentas/README.md) (F12).

## 0. Premissa: Cursor primeiro
Todo o desenvolvimento acontece no **Cursor**: código, regras, agentes e PRs. A plataforma **não é IDE nem ambiente de desenvolvimento**. Ela é um painel de visualização com poucas funções úteis: ver, filtrar, alertar e levar ao lugar certo (PR, issue, painel do serviço, documento do catálogo). Quando houver alteração, ela acontece no Git (YAML/PR) feito no Cursor, nunca editando direto na plataforma.

## 1. Objetivos
1. Mostrar **onde está cada projeto** e o que está travado.
2. Mostrar **o que cada agente fez e para quem passou** (handoffs do [SOP](../processos/fluxo-entre-agentes.md)).
3. Mostrar **ferramentas e conexões de cada projeto** e se estão saudáveis.
4. Concentrar **o que depende do Samuel** em uma fila única de aprovações.
5. Registrar **decisões** dos agentes ("decidir o mínimo, documentar sempre").
6. Medir **ritmo, qualidade e custo** (cota de tokens, saldo do Cursor, planos dos serviços) e **alertar** antes do problema.

Fora do objetivo: substituir o GitHub, o Cursor ou o backlog YAML, e guardar segredos.

## 2. Usuários
| Usuário | Uso | Permissão |
|---|---|---|
| Samuel (dono/aprovador) | Visão geral, aprovações, decisões, conexões, custos | Leitura total; aprova pelo GitHub |
| Orquestrador | Status, handoffs, alertas | Escreve só no `vtx-core` (YAML via PR/commit) |
| Demais papéis ([agents/](../../agents/README.md)) | Eventos, decisões, manifestos de conexão | Escrevem via YAML/PR |
| Público | Só o [painel público](https://samalencar.github.io/vtx_painel/) sanitizado | Sem acesso |

## 3. Módulos
| # | Módulo | Conteúdo | Etapa |
|---|---|---|---|
| 1 | Portfólio | Projetos, tipo (triagem), fase, % concluído, próxima tarefa, bloqueios | MVP |
| 2 | Backlog e fases | Status efetivo, dependências, tarefas paradas | MVP |
| 3 | **Ferramentas e conexões por projeto** | Ver §4 | MVP |
| 4 | Atividade dos agentes | Linha do tempo por papel, handoffs, devoluções, retrabalho | Web |
| 5 | Fila de aprovações | Portões pendentes (fluxos, `mvp-poc` §3, SOP §5), prazo, link para aprovar | Web |
| 6 | Registro de decisões | Decisão, autor, motivo, reversível?, escalado ou não | Web |
| 7 | Métricas e custos | Vazão, lead time, retrabalho, CI; cota Grok Bot, saldo Cursor, planos ativos | Web |
| 8 | Alertas | Tarefa parada > 1 dia, aprovação vencida, CI vermelha, conexão quebrada ou expirando, cota > 80% | MVP (no resumo diário) |

## 4. Ferramentas e conexões por projeto
**Manifesto por projeto** em `projects/<p>/conexoes.yaml` no `vtx-core`. O manifesto fica no `vtx-core`, e não no repositório do projeto, porque assim o leitor usa uma fonte única e um só token de leitura, e os repositórios de cliente não precisam ser acessados. O esquema é documentado em `projects/CONEXOES.md` e validado no CI (VTX-115).

```yaml
projeto: plataforma-projetos
conexoes:
  - id: repo
    ferramenta: github            # id do catálogo (knowledge/ferramentas/)
    recurso: SamAlencar/plataforma-projetos
    ambiente: producao            # desenvolvimento | homologacao | producao
    responsavel: devops-sre       # papel de agents/
    segredo_ref: "GitHub secret PANEL_TOKEN"   # SÓ a referência de onde está; nunca o valor
    verificacao: {tipo: github_api}            # github_api | http | tls | dns | manual
    expira_em: null               # token/domínio/certificado, se houver
  - id: site
    ferramenta: vercel
    recurso: https://exemplo.vercel.app/api/health
    ambiente: producao
    responsavel: devops-sre
    verificacao: {tipo: http, esperado: 200}
```
- **Estado** (gerado pelo verificador, fora do manifesto): `ok | degradado | quebrado | desconhecido`, `ultima_verificacao`, `detalhe`.
- **Verificador (VTX-116):** workflow agendado em `vtx-acompanhamento`, **somente leitura**. Na etapa 1 só usa o que dispensa segredo novo: API do GitHub (token já existente, escopo mínimo), endpoint HTTP de saúde, validade de TLS e de domínio, DNS. Verificações por API de serviços (Vercel, Supabase, Sentry...) entram depois, uma a uma. Cada token novo precisa de escopo de leitura e é criado na conta do Samuel, com aprovação dele.
- **Alertas:** conexão `quebrada`, sem verificação há mais de 48 h, ou expirando em até 30 dias (token, domínio, certificado, plano gratuito no limite).
- **Ligação ao catálogo:** cada `ferramenta` aponta para o documento dela em `knowledge/ferramentas/`. Ferramenta fora do catálogo gera aviso, e adotá-la segue os critérios do catálogo, §4.
- **Segurança:** valores de segredo nunca entram no manifesto, no JSON ou na tela, só a referência de onde estão (`segredo_ref`). Para clientes, nada de dados pessoais.

## 5. Fontes de dados
| Dado | Fonte (verdade) | Situação |
|---|---|---|
| Projeto, fases, tarefas | `backlog/` ([SCHEMA](../../backlog/SCHEMA.md)) via `scripts/backlog_lib.py` | Existe |
| Eventos/handoffs, decisões, custos | `registro/eventos/AAAA-MM-DD.yaml`, `registro/decisoes.yaml`, `registro/custos.yaml` (VTX-087) | A criar |
| Aprovações | `registro/aprovacoes.yaml` + rótulo `aprovacao-samuel` (VTX-088, alinhado à VTX-064) | A criar |
| Conexões | `projects/<p>/conexoes.yaml` + estado gerado pelo verificador | A criar |
| Ferramentas | `knowledge/ferramentas/` (F12) | Em andamento |
| CI e commits | API do GitHub | Existe |

## 6. Arquitetura (revisada)
Um painel só em Markdown não basta para um ambiente completo, porque não dá para filtrar, cruzar projeto × conexão × alerta nem usar bem no celular. Decisão conservadora:
1. **Contrato único:** o gerador produz `plataforma.json` (privado). Todas as telas leem esse JSON, e nenhuma escreve.
2. **Semana 1, Markdown privado:** portfólio, fases e conexões em `vtx-acompanhamento/painel/*.md`. Custo zero, serve para validar dados e verificador.
3. **Logo depois, interface web restrita** (o ADR VTX-095 foi antecipado para depois do Markdown). Recomendação: **site estático** (sem backend) sobre o mesmo JSON, publicado com **login obrigatório** em hospedagem com controle de acesso. Opções no ADR: Cloudflare Pages + Access, ou Vercel com proteção de deploy. Preferir plano gratuito e conferir no ADR os limites, os termos de uso comercial e a exigência de cartão.
4. **Supabase + auth só se justificado:** quando houver necessidade comprovada de histórico consultável (séries de status) ou de ações gravadas. Por enquanto o histórico fica em arquivos no repositório.
5. **Ações:** continuam no GitHub (review de PR, issue). A plataforma só mostra o link.

Fica descartado neste momento: backend próprio, edição pela plataforma e qualquer forma de IDE.

## 7. Segurança
- Nada sensível no `vtx_painel` público.
- Tokens de leitura com escopo mínimo, em secrets do GitHub, nunca no chat ou no repositório. O manifesto guarda só a referência.
- Interface web somente com login. URL sem login = bloqueio de release.
- O gerador e o verificador nunca escrevem no `vtx-core` nem nos serviços verificados.

## 8. Precisa do Samuel
- **Qualquer custo recorrente ou cartão** (hospedagem, plano pago, domínio próprio).
- **Conta/serviço novo** para a interface web e a escolha do provedor (ADR VTX-095).
- **Criação de tokens** de leitura nos serviços dele (Vercel, Supabase, Sentry...) para o verificador.
- Portões do `mvp-poc`: hipóteses (VTX-086) e decisão continuar/pivotar (VTX-094).

## 9. Como segue os fluxos da VTX
| Etapa `mvp-poc` | Tarefas |
|---|---|
| 1 Descoberta | Este documento |
| 2 Hipóteses (**portão Samuel**) | VTX-086 (ex.: "acompanho tudo, inclusive conexões, em ≤ 5 min/dia") |
| 3 Experimento | VTX-087, 088, 115: formatos |
| 4 Construção | VTX-089, 116, 090, 117 (Markdown) → VTX-095 (ADR, **portão Samuel**) → VTX-096, 091, 092, 118, 093 (web) |
| 5 a 6 Medição e decisão (**portão Samuel**) | VTX-094 |
| 7 Transição | VTX-097 (projetos de cliente) |

Papéis: Orquestrador (fluxo e registros), Produto (PRD), Arquiteto (formatos, ADR), Dev Backend (gerador, verificador), Dev Frontend (telas), QA (testes e sanitização), DevOps/SRE (workflows, tokens, conexões), AppSec (revisão do login e dos tokens).

## 10. Plano conjunto com a base de conhecimento
- Formatos novos (`registro/`, `projects/*/conexoes.yaml`) nascem no `vtx-core`, documentados e validados no CI.
- **Depende da F12:** ids de ferramenta e verificações sugeridas vêm do catálogo (VTX-098). A tela de conexões (VTX-118) usa a matriz completa (VTX-112).
- Consome VTX-014, 038, 063, 064 e 073. Lições voltam à base na retrospectiva.

## 11. Posição no backlog
A F11 fica entre a F9 e a F8, prioridades 83 a 100. A F8 e a F10 vão de 101 a 117, mantendo a ordem relativa. A F12 (catálogo) vem antes, nas prioridades 36 a 51, o que atende à dependência. Se a F9 for antecipada, a F11 continua logo depois dela.

## Fontes
- Base VTX: [SOP](../processos/fluxo-entre-agentes.md), [MVP/PoC](../processos/fluxos/mvp-poc.md), [catálogo de ferramentas](../ferramentas/README.md), [SCHEMA](../../backlog/SCHEMA.md).
- GitHub Docs: "About GitHub Pages" (sites de repositórios privados são públicos fora do Enterprise); "fine-grained personal access tokens".
- Forsgren, Humble e Kim, *Accelerate* (métricas).
