# Comunicação e gestão: Google (Gmail, Drive, Agenda, Meet) e Grok Bot
> Comunicação e gestão · Status: **adotado** (conta Google grátis da VTX + chat do Grok Bot); Workspace pago só com domínio e A2 · Revisado em 2026-11-01 · VTX-111

## 1. O que é
- **Google:** a VTX usa uma conta Google grátis (`samuel.vtxsystems@gmail.com`, conferida em 01/11) com Gmail, Drive (pasta "VTX - Empresa de Agentes IA"), Agenda e Meet. O Google Workspace pago é a mesma suíte com e-mail no domínio próprio, administração central e mais armazenamento.
- **Grok Bot:** assistente onde os agentes da VTX rodam rotinas (tarefa diária, resumo semanal, manutenção), leem Gmail/Drive/Agenda pelos conectores e falam com Samuel no chat. É o único canal com Samuel.

## 2. Quando usar / quando não usar
- **Usar:** relatório semanal e documento para Samuel ou cliente (Docs no Drive, `04 - Relatórios`); material recebido do cliente (Drive do projeto); entrevista e reunião (Agenda + Meet); avisos e perguntas a Samuel (chat do Grok Bot).
- **Não usar:** como fonte da verdade técnica (código, backlog e base de conhecimento ficam no GitHub, `vtx-core`); para segredo ou senha; para mandar e-mail a cliente sem pedido explícito de Samuel.

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Workspace Business Starter | e-mail no domínio próprio (ex.: site-vtx no ar) | A2; cobra por usuário |
| Zoho Mail Free / Cloudflare Email Routing | e-mail no domínio sem custo | encaminha para o Gmail; sem suíte |
| Nextcloud (AGPL) | cliente exige self-host | arquivos e agenda no próprio servidor |
| GitHub Issues/Discussions | conversa técnica | fica junto do código |

## 4. Custo e plano gratuito (conferido em 01/11/2026)
- **Conta Google grátis:** 15 GB compartilhados entre Gmail, Drive e Fotos; Meet incluso (limites do grátis conferir antes de reunião longa com cliente). Sem custo hoje.
- **Workspace (página pt-BR, em US$):** Business Starter US$ 7/usuário/mês (promoção de US$ 3,50 por 12 meses para os primeiros 20 usuários de cliente novo), 30 GB em pool por usuário, Meet até 100 pessoas; Standard US$ 14. Exige domínio e é custo novo: A2.
- **Grok Bot:** cota semanal compartilhada entre todos os agentes de Samuel; a rotina diária reduz tarefas quando a cota passa de ~70% antes de quinta.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [Entrevista com o cliente](../../processos/fluxos/entrevista-cliente.md) | descoberta | Agenda + Meet; ata no Drive |
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | acompanhamento | relatório semanal no Drive; aprovação A2 no chat |
| [Site](../../processos/fluxos/site-landing-page.md) | conteúdo | textos e imagens do cliente no Drive |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | chamado | e-mail do cliente vira issue no GitHub |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | demonstração | link do Meet e roteiro no Drive |

## 6. Papel responsável
Orquestrador escreve relatórios no Drive e fala com Samuel pelo Grok Bot ([orquestrador](../../../agents/orquestrador.md)); Produto conduz entrevistas; demais agentes só leem o Drive do projeto; Samuel decide envio externo, compartilhamento fora da VTX e qualquer plano pago.

## 7. Setup
1. Drive: pasta por projeto dentro de "VTX - Empresa de Agentes IA" (`01 - Gestão`, `04 - Relatórios`, material do cliente); compartilhar com o cliente só a pasta dele, como leitor ou comentarista.
2. Documento para humano no Drive; conhecimento reutilizável vai para o repo e o Drive só aponta para ele (sem duplicar).
3. Agenda: evento com link do Meet e pauta; ata no Drive no mesmo dia.
4. Grok Bot: uma rotina por cadência (diária, semanal, quinzenal) com prompt de intenção; mensagem curta em pt-BR com links e o [painel](https://samalencar.github.io/painel-central/).
5. E-mail ao cliente: rascunho para Samuel aprovar; envio só com pedido explícito.

## 8. Segredos e segurança/LGPD
- 2FA na conta Google; acesso dos agentes só pelos conectores do Grok Bot (OAuth), nunca senha em arquivo.
- Nada de senha, token ou chave em Doc, e-mail ou chat; segredo vai no gerenciador do projeto ou em segredo do GitHub.
- Dado pessoal de cliente só na pasta do projeto, com acesso mínimo; apagar ao fim do contrato conforme combinado.
- Conta grátis não tem DPA de Workspace nem região de dados escolhível: para cliente com exigência de LGPD formal, propor Workspace (A2).

## 9. Checklist
- [ ] Pasta do projeto no Drive com permissão mínima
- [ ] Relatório semanal no `04 - Relatórios`
- [ ] Reunião com Meet e ata no Drive
- [ ] Nenhum segredo em Doc, e-mail ou chat
- [ ] Envio externo só com pedido de Samuel
- [ ] Armazenamento (15 GB) acompanhado; plano pago só com A2

## 10. Registro de avaliação e Fontes
**ADR curto (01/11/2026):** *Contexto:* VTX ainda sem domínio de e-mail e sem receita. *Opções:* conta Google grátis, Workspace Business Starter, Zoho/Nextcloud. *Decisão:* manter a conta grátis + Grok Bot; Workspace só quando houver domínio e primeiro cliente pagante (A2). *Consequência:* revisar ao publicar o site-vtx.
- Preços do Workspace: https://workspace.google.com/intl/pt-BR/pricing.html
- Armazenamento da conta Google: https://support.google.com/googleone/answer/9312312
- Cloudflare Email Routing: https://developers.cloudflare.com/email-routing/
- Nextcloud: https://github.com/nextcloud/server
