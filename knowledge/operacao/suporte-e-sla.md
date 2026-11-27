# Pacote técnico de manutenção, SLA e suporte

> VTX-199 · Fase F14 · Operação. Lado técnico do suporte previsível (sem preço nem venda). Complementa [DevOps e SRE](devops-sre.md) (SLOs e incidentes), o [fluxo de manutenção e evolução](../processos/fluxos/manutencao-evolucao.md) e o [runbook do template web](../../templates/web-next/docs/runbook.md). Preço e comercialização do plano de manutenção são dependência externa (agentes de vendas).

## 1. Conceitos

- **SLA técnico:** compromisso de *tempo de resposta* e *horas de esforço incluídas* por período, por nível. Não é SLO de produto (disponibilidade/latência — isso fica em [devops-sre.md](devops-sre.md) e no PRD).
- **Dois níveis padrão:** *Essencial* (reação a incidente e bugs bloqueantes) e *Evolução* (Essencial + melhorias pequenas e preventivas dentro das horas).
- **Canal único de entrada:** e-mail ou formulário do projeto; triagem por agente; humano (Samuel) só em A2.
- **Postmortem curto:** após SEV1/SEV2 (ou recorrência SEV3), um arquivo no repositório do *cliente*, sem culpados, com ações no backlog.
- **Monitor gratuito:** verificação externa de disponibilidade no plano free; alerta chega no canal de suporte.

## 2. Dois níveis de SLA

Valores iniciais da VTX; o contrato do cliente pode apertar, nunca afrouxar sem A2. Horas são de *esforço de agente + revisão*, não de relógio corrido 24×7.

| Nível | Tempo de 1ª resposta | Horas incluídas / mês | Escopo típico | Fora do escopo |
|---|---|---|---|---|
| **Essencial** | SEV1: 4 h úteis · SEV2: 1 dia útil · SEV3: 3 dias úteis | 4 h | Incidente, bug bloqueante, regressão de segurança, restore orientado | Nova funcionalidade, redesign, migração de stack |
| **Evolução** | Mesmos tempos do Essencial | 12 h | Essencial + perfectiva/preventiva pequena (deps, correção de UX, ajuste de relatório) | Projeto novo, mudança de provedor pago, campanha |

**Regras comuns**

- **Horário útil VTX:** dias úteis, 9h–18h (America/Sao_Paulo), salvo acordo explícito no PRD.
- **Estouro de horas:** agente registra no diário do projeto, classifica A2 e *para* trabalho não-SEV1 até o Samuel autorizar hora extra ou próximo ciclo.
- **Resposta ≠ resolução:** a 1ª resposta confirma recebimento, severidade e próximo passo; o prazo de correção segue o diagnóstico (fluxo de manutenção).
- **Dois relógios, uma verdade:** os *tempos da tabela de níveis* acima são o **compromisso contratual de 1ª resposta** com o cliente (fonte deste documento). A **meta interna de mitigação** fica em [devops-sre.md](devops-sre.md): SEV1 imediata, SEV2 em ≤ 1 h, SEV3 no próximo ciclo. A equipe persegue a meta interna primeiro; o SLA contratual é o teto que o cliente pode cobrar. Os *exemplos* de Sev e o aviso ao Samuel são os mesmos nos dois documentos.

| Sev | Exemplo | Quem age | Avisar Samuel |
|---|---|---|---|
| SEV1 | Produção fora do ar, perda de dados, vazamento | DevOps/SRE + Dev; rollback sem esperar | na hora |
| SEV2 | Função crítica degradada, workaround difícil | Dev + QA | no mesmo dia |
| SEV3 | Bug menor, dúvida operacional, pedido de melhoria | Triagem → backlog ou resposta direta | relatório semanal |

## 3. Canal de suporte e triagem por agente

### 3.1 Entrada

Um canal por projeto (não misturar clientes):

1. **E-mail dedicado** `suporte+<projeto>@…` *ou*
2. **Formulário** na área logada / página de status (template site ou web-next), que grava issue ou e-mail.

O endereço e o link ficam no `docs/runbook.md` do projeto e no README do cliente.

### 3.2 Fluxo de triagem (agente)

| Passo | Quem | Artefato | Portão |
|---|---|---|---|
| 1. Receber | Agente de triagem | Ticket bruto (assunto, texto, anexos sem segredo) | — |
| 2. Classificar | Agente de triagem | Sev, tipo (incidente / bug / dúvida / evolução), projeto | Checklist §7 |
| 3. Responder 1ª | Agente de triagem | Confirmação no mesmo canal + link do ticket | Dentro do SLA de resposta |
| 4. Encaminhar | Orquestrador | Item no backlog do cliente ou ação imediata SEV1 | SEV1: DevOps sem esperar; demais: dono do papel |
| 5. Fechar | Quem executou | Resumo no ticket + changelog se houve release | SEV1/2: postmortem se §5 exigir |

- Dado pessoal ou segredo no ticket → não copiar para prompt/chat; redigir e seguir [governança](../processos/governanca-e-aprovacoes.md).
- Pedido de novo projeto ou mudança de escopo grande → não consome horas de manutenção; vira triagem de projeto ([triagem.md](../processos/fluxos/triagem.md)).

## 4. Monitor de disponibilidade (gratuito)

Configuração mínima no *template* e em todo projeto em produção:

| Item | Padrão VTX (plano free) |
|---|---|
| O quê | HTTP(S) 200 no health (`/api/health` ou `/`) a cada 5 min |
| Onde | [UptimeRobot](https://uptimerobot.com/) ou [Better Stack Uptime](https://betterstack.com/uptime) (tier gratuito) |
| Alerta | E-mail do canal de suporte do projeto (e opcionalmente webhook → issue) |
| Quem configura | DevOps no go-live; registra URL do monitor no `docs/runbook.md` |
| Limite | Sem SMS pago e sem dezenas de monitores extras sem A2 |

Falha consecutiva (ex.: 2 ciclos) = SEV1 operacional até prova em contrário. O monitor *não* substitui logs/Sentry ([observabilidade](observabilidade.md)).

O template web-next ainda não tem a rota `/api/health`. Até ela existir, o monitor aponta para `/` (já responde sem autenticação) e o runbook registra essa escolha.

## 5. Incidentes → postmortem curto no repo do cliente

Obrigatório após SEV1 e SEV2 (e SEV3 se repetir ≥ 3 vezes no mês), em até 5 dias úteis (prazo em [devops-sre.md](devops-sre.md)). O arquivo fica no **repositório do cliente** (não em `projects/` no vtx-core):

`docs/postmortems/AAAA-MM-DD-titulo.md`

O modelo no template web-next é `templates/web-next/docs/postmortems/0000-modelo.md`; no repositório gerado, `docs/postmortems/0000-modelo.md`.

Modelo mínimo:

```markdown
# Postmortem: <título curto>
- Data do incidente:
- Sev:
- Duração (detectado → mitigado):
- Impacto (usuários / dados / dinheiro):

## Linha do tempo
- HH:MM — …

## Causa raiz (sistêmica)
…

## O que funcionou / o que falhou
…

## Ações (viram item de backlog)
| Ação | Dono | Prazo |
|---|---|---|
| | | |
```

Regras: sem culpados; ações rastreáveis no backlog; se a ação for na base VTX (template, SOP), abre tarefa no `vtx-core` também. Detalhe de SEV e rollback: [devops-sre.md](devops-sre.md).

## 6. Exemplo

Cliente no nível **Essencial**. Segunda, 10h: monitor acusa o health (ou `/`, se a rota `/api/health` ainda não existir) em 502. Agente de triagem abre SEV1, responde no e-mail em 20 min, aciona DevOps. Rollback no painel da Cloudflare Pages (padrão do [runbook](../../templates/web-next/docs/runbook.md); Vercel só se o projeto já tiver Pro aprovado em A2) restaura o serviço às 10:45. Postmortem no repositório do cliente no mesmo dia; ação: “teste de smoke no pipeline antes do promote” → item no backlog. Quarta: pedido de “tela nova de relatório” — fora do Essencial; agente orienta pacote de evolução ou novo incremento, sem consumir as 4 h em feature.

## 7. Checklist

- [ ] Nível de SLA (Essencial ou Evolução) registrado no PRD / ficha do projeto
- [ ] Tempos de 1ª resposta e horas/mês explícitos
- [ ] Canal único de suporte no runbook e no README do cliente
- [ ] Triagem por agente com classificação de severidade
- [ ] Monitor HTTP gratuito ativo em produção; alerta no canal de suporte
- [ ] Health check documentado (`/api/health` ou equivalente)
- [ ] SEV1/SEV2 geram postmortem curto no repositório do *cliente*
- [ ] Estouro de horas ou upgrade de nível → A2 (Samuel)
- [ ] Preço/venda do plano *não* tratados neste documento (dependência externa)

## Fontes

- Google, *Site Reliability Engineering* — postmortem e SLOs: https://sre.google/sre-book/table-of-contents/
- PagerDuty, *Incident Response Guide* (processo, ferramenta não adotada): https://response.pagerduty.com/
- ISO/IEC/IEEE 14764:2022 (tipos de manutenção) — ver também [manutenção e evolução](../processos/fluxos/manutencao-evolucao.md)
- UptimeRobot (monitor gratuito): https://uptimerobot.com/ · Better Stack Uptime: https://betterstack.com/uptime
- [Governança e aprovações](../processos/governanca-e-aprovacoes.md) · [DevOps e SRE](devops-sre.md) · [Observabilidade](observabilidade.md)
