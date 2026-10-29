# Cursor
> IA para desenvolvimento · Status: **adotado** (IDE e agentes de toda a VTX; Cloud Agents só com real necessidade) · Revisado em 2026-10-29 · VTX-102

## 1. O que é
Editor com agente de IA onde os agentes da VTX programam. Lê **regras** (`.cursor/rules/*.mdc` e `AGENTS.md`), **skills** (`.cursor/skills/<nome>/SKILL.md`), servidores **MCP** e roda em três modos: no editor, na **CLI** (`agent -p "..."`, sem interação) e em **Cloud Agents** (VM na nuvem que clona o repo e abre PR). As regras-padrão da VTX estão na F9: [Regras do Cursor](../../templates/cursor/README.md).

## 2. Quando usar / quando não usar
- **Usar:** todo trabalho de código e documentação dos projetos; CLI para tarefas de rotina sem tela; regras e skills para fixar o "jeito VTX".
- **Não usar:** Cloud Agent para tarefa que roda na máquina local (custo); regra para conhecimento longo (vai para `knowledge/` e é referenciado).

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Modo local (agente do Grok Bot no box, git/gh) | padrão desde 17/10/2026 | não gasta saldo sob demanda; mesmo rigor de PR e CI |
| Cloud Agent | tarefa impossível no box (ex.: ambiente que não sobe localmente) | paralelo e isolado, mas consome uso/saldo |
| VS Code + extensão open source | cliente exige outro editor | regras viram `AGENTS.md`, que é formato aberto |

## 4. Custo e plano (conferido em 29/10/2026)
- Uso dos agentes sai de um **pool** do plano (renova semanalmente nos planos novos; mensal nos legados). Cloud Agents consomem esse pool na taxa do modelo e pedem limite de gasto no primeiro uso.
- Planos legados (Pro etc.) têm **saldo sob demanda** cobrado depois; o da conta do Samuel estourou em 17/10 (renova ~09/11/2026).
- **Regra VTX:** não lançar Cloud Agent nem depois da renovação, salvo real necessidade registrada no log ("[geral] agente na nuvem: <motivo>"). Mudar plano ou ligar gasto é **decisão do Samuel (A2)**.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | implementação → PR | agente com regras do repo; uma tarefa por branch |
| [Mobile](../../processos/fluxos/app-mobile.md) | implementação | idem; testes em emulador ficam fora do agente |
| [API](../../processos/fluxos/api-integracoes.md) | contrato → código | MCP de docs (Supabase, Appwrite, Stripe) como fonte |
| [Site](../../processos/fluxos/site-landing-page.md) | build | skills de UX/frontend do catálogo |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | correção | CLI `agent -p` em rotina; diff revisado antes do merge |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | protótipo | sessão curta, sem regra nova |

## 6. Papel responsável
Orquestrador mantém regras e skills do vtx-core e decide modo (local ou nuvem); cada Dev usa as regras do repo; QA confere que o agente rodou os testes; Samuel aprova plano e gasto ([papéis](../../../agents/)).

## 7. Setup (por repositório)
1. Copiar a base da F9: `.cursorignore` na raiz e `eficiencia-de-tokens.mdc` em `.cursor/rules/` ([templates](../../templates/cursor/README.md)).
2. Regras: `.mdc` com frontmatter `description`, `globs`, `alwaysApply`. Quatro tipos: sempre, inteligente (pela descrição), por arquivo (glob) e manual (`@regra`). `.md` solto em `.cursor/rules` é ignorado; prosa simples vai em `AGENTS.md`. Cada regra < 500 linhas; `alwaysApply: true` só para o que vale em todo turno ([operação de agentes](../../processos/operacao-de-agentes.md)).
3. Skills: `.cursor/skills/<nome>/SKILL.md` (no vtx-core: `writing-plans`, `brainstorming`, `verification-before-completion`), fixadas por versão e revisadas como biblioteca ([recursos](../recursos.yaml)).
4. MCP: só servidores do catálogo, com escopo mínimo (ex.: Supabase `read_only`, [Supabase](../backend/supabase.md)).
5. Modo local: clone em `/workspace/repos/<repo>`, branch `local/<ID>-<slug>`, checks da CI rodados antes do PR (`/workspace/tekto-modo-local.md`).

## 8. Segredos e segurança/LGPD
- `.cursorignore` bloqueia `.env*`, chaves e dados de cliente; segredo nunca em regra, skill, prompt ou chat.
- Cloud Agent: segredos só na aba Secrets do painel; nada de `.env.local` em snapshot nem em `.cursor/environment.json`.
- Conteúdo lido por MCP, web ou issue é não confiável (*prompt injection*): o agente não executa ordem vinda dele.
- Dado pessoal de cliente fora do contexto do agente, salvo anonimizado ([desenvolvimento seguro](../../seguranca/desenvolvimento-seguro.md)).

## 9. Checklist
- [ ] `.cursorignore` e regra de tokens da F9 no repo
- [ ] Regras em `.mdc` com tipo correto; nenhuma sempre-ativa desnecessária
- [ ] Skills com versão fixada e revisadas
- [ ] MCPs do catálogo, com escopo mínimo
- [ ] Trabalho em modo local; Cloud Agent só com motivo registrado
- [ ] Nenhum segredo em regra, skill, snapshot ou chat

## 10. Registro de adoção e Fontes
**ADR curto (29/10/2026):** *Contexto:* agentes da VTX trabalham no Cursor; saldo sob demanda estourou em 17/10. *Opções:* Cloud Agents, modo local, outro editor. *Decisão:* Cursor com regras/skills no repo e execução em modo local; Cloud Agent como exceção registrada. *Consequência:* custo previsível; paralelismo menor.
- Regras: https://cursor.com/docs/context/rules
- Skills: https://cursor.com/docs/context/skills
- Arquivos ignorados: https://cursor.com/docs/context/ignore-files
- MCP: https://cursor.com/docs/context/mcp
- CLI: https://cursor.com/docs/cli/overview
- Cloud Agents (cobrança e segredos): https://cursor.com/docs/cloud-agent
- Planos e uso: https://cursor.com/docs/models-and-pricing
