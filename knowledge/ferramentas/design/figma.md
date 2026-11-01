# Figma
> Design · Status: **recomendado** (handoff de telas e sites; Starter grátis com limites) · Revisado em 2026-11-01 · VTX-110

## 1. O que é
Editor de interface no navegador (Design, protótipos, FigJam) com inspeção para dev, variáveis (tokens) e um servidor MCP remoto que entrega o contexto de um frame ao Cursor. Já conectado à VTX desde 23/10/2026 ([stack](../../tecnologia/stack-de-referencia.md)). É fonte do design, não do código: os tokens viram Tailwind e os componentes viram shadcn/ui ([frontend](../../tecnologia/frontend-web.md)).

## 2. Quando usar / quando não usar
- **Usar:** telas de produto e sites (site-vtx, site-med-hub, site-tekto) antes do código; protótipo para o cliente aprovar; tokens de cor, tipografia e espaçamento; FigJam para fluxo e mapa de telas.
- **Não usar:** como documentação de regra de negócio (vai no PRD); tela simples que o design system já resolve; quando o cliente exige ferramenta self-host (usar Penpot).

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Penpot (MPL-2.0) | cliente quer self-host ou sem limite de arquivo | open source, tem MCP oficial; menos plugins |
| Excalidraw | rascunho e diagrama rápido | grátis, sem conta |
| Direto no código (shadcn/ui) | tela interna, CRUD | o design system já decide |

## 4. Custo e plano gratuito (conferido em 01/11/2026)
- **Conta conectada:** "Samuel's team", plano **Starter**, assento Full (consulta `whoami` do MCP em 01/11).
- **Starter (grátis):** 1 pasta com 3 arquivos de Design/Sites, 3 FigJam e 3 Slides; rascunhos ilimitados (sem coeditor, só leitores); 30 dias de histórico; sem Dev Mode, bibliotecas de time, ramificação nem Code Connect; IA 150 créditos/dia até 500/mês. Inspeção básica (medidas, CSS, exportar) funciona para leitor.
- **MCP no Starter:** até **20 chamadas de leitura por mês** (ferramentas de escrita como `create_new_file` e `whoami` não contam). Gastar só no handoff final de cada tela, nunca para explorar.
- **Professional:** assento Full US$ 16/mês, Dev US$ 12/mês; MCP até 200 chamadas/dia e 10/min, Dev Mode e bibliotecas (A2).

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [Site](../../processos/fluxos/site-landing-page.md) | design e aprovação | layout e protótipo; handoff por MCP |
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | UX/UI | telas com os 4 estados (carregando, vazio, erro, sucesso) |
| [Mobile](../../processos/fluxos/app-mobile.md) | UX/UI | telas e protótipo navegável |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | demonstração | protótipo clicável no lugar de código |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | melhoria visual | só a tela alterada |

## 6. Papel responsável
Produto/UX desenha e organiza; Dev Frontend consome pelo MCP e converte tokens; QA compara tela pronta com o frame; Samuel aprova plano pago e compartilhamento com cliente ([papéis](../../../agents/)).

## 7. Setup
1. Um arquivo por projeto na pasta do time (Starter: 3 no máximo; arquivar o concluído em `.fig` no Drive do projeto para liberar vaga).
2. Páginas fixas: `Tokens`, `Componentes`, `Telas`, `Protótipo`; frames nomeados como as rotas.
3. Variáveis de cor/tipografia/espaçamento com os mesmos nomes do `tailwind.config`.
4. Handoff: copiar link do frame ("Copy link to selection") e passar ao Cursor com o MCP do Figma; uma chamada por tela, anotada no PR.
5. Marcar versão nomeada ao aprovar (histórico só 30 dias no Starter); exportar PNG da tela aprovada para o PR.

## 8. Segredos e segurança/LGPD
- Sem dado real de cliente (nome, CPF, e-mail) nas telas: usar dado fictício.
- Link do arquivo "só convidados"; leitor externo só por convite com e-mail.
- Token pessoal do Figma, se precisar da REST API, fica em segredo do CI, nunca no repo.
- Arquivos ficam nos servidores do Figma (EUA): constar como suboperador quando o cliente envia material.

## 9. Checklist
- [ ] Arquivo do projeto criado (vaga no Starter conferida)
- [ ] Tokens com nomes iguais aos do Tailwind
- [ ] Telas com os 4 estados
- [ ] Versão nomeada na aprovação e PNG no PR
- [ ] Chamadas do MCP do mês contadas (≤ 20)
- [ ] Sem dado real de cliente; link restrito

## 10. Registro de avaliação e Fontes
**ADR curto (01/11/2026):** *Contexto:* Figma já conectado; conta no Starter. *Opções:* Starter, Professional (A2), Penpot. *Decisão:* seguir no Starter, com MCP reservado ao handoff final e arquivos rotativos; Penpot quando o cliente exigir self-host. *Consequência:* passar de 20 chamadas/mês ou de 3 arquivos ativos é sinal para pedir A2 do Professional (Dev seat US$ 12).
- Preços: https://www.figma.com/pricing/
- Plano Starter: https://help.figma.com/hc/en-us/articles/13838684089751-Starter-plan-overview
- Planos e recursos: https://help.figma.com/hc/en-us/articles/360040328273-Figma-plans-and-features
- Limites do MCP: https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/
- MCP remoto: https://help.figma.com/hc/en-us/articles/35281350665623-Figma-MCP-collection-How-to-set-up-the-Figma-remote-MCP-server
- Penpot: https://github.com/penpot/penpot · MCP: https://github.com/penpot/penpot-mcp
