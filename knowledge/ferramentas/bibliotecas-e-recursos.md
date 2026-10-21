# Bibliotecas e recursos para agentes

> VTX-119 · Fase F12 · Ferramentas. Este documento explica como a VTX **descobre, avalia, registra e usa** bibliotecas, skills, regras e servidores MCP que melhoram o trabalho dos agentes. Complementa o [catálogo de ferramentas](README.md): ferramenta = serviço (Vercel, Supabase); recurso = algo que o agente usa dentro do projeto. O registro fica em [`recursos.yaml`](recursos.yaml).

## 1. Exemplo de referência: Impeccable
[pbakaus/impeccable](https://github.com/pbakaus/impeccable) ([site](https://impeccable.style)), Apache-2.0, cerca de 82 mil estrelas, ativo em 17/10/2026. É um conjunto de orientação de design para agentes de código: **1 skill, 24 comandos** (`/impeccable init`, `shape`, `critique`, `audit`, `polish`, `harden`...) e **59 regras determinísticas** que detectam os "vícios" visuais típicos de frontend gerado por IA. O `init` cria um `PRODUCT.md` com o contexto do produto. Instala com `npx impeccable install --providers=cursor --scope=project`, que coloca a skill e hooks em `.cursor`, e funciona também com Grok Build, Claude Code e Codex. **Status: em avaliação.** É gratuito e serve ao fluxo de frontend, mas baixa um binário no primeiro uso e instala hooks, o que exige revisão de segurança e piloto em sandbox (VTX-127).

## 2. Descoberta (onde procurar)
| Tipo de fonte | Exemplos verificados |
|---|---|
| Repositórios de skills (git, inspecionáveis) | [anthropics/skills](https://github.com/anthropics/skills), [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), impeccable, [mattpocock/skills](https://github.com/mattpocock/skills), [emilkowalski/skills](https://github.com/emilkowalski/skills); descoberta via [skills.sh](https://skills.sh) (aponta para o repo) |
| Marketplaces MCP remotos de skills | [Agensi](https://www.agensi.io/) e similares — **descartados por enquanto** (ver §3.1) |
| Coleções de regras do Cursor | [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) |
| Registros de MCP | [MCP Registry oficial](https://registry.modelcontextprotocol.io), [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers), [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) |
| Bibliotecas de componentes | [shadcn/ui](https://github.com/shadcn-ui/ui) |
| Referências por área | [OWASP Cheat Sheets](https://github.com/OWASP/CheatSheetSeries) |
| Listas "awesome" | [sindresorhus/awesome](https://github.com/sindresorhus/awesome) (índice de listas por tema) |

**Varredura periódica:** na manutenção quinzenal, olhar as fontes acima atrás de novidades em 1 ou 2 áreas, em rodízio, com no máximo 3 candidatos por ciclo. Na revisão trimestral (VTX-113), reavaliar os itens adotados e descartar os que não estão em uso.

## 3. Avaliação (antes de entrar como candidato)
1. **Licença:** MIT, Apache-2.0, BSD e CC0 são aceitas. CC-BY e CC-BY-SA só para referência, com atribuição. Sem licença ou com licença restritiva: não copiar. Em repositórios mistos (ex.: anthropics/skills), conferir a licença **de cada skill** — as de documento (`docx`, `pdf`, `pptx`, `xlsx`) são source-available sob termos da Anthropic, **não** open source: não copiar.
2. **Manutenção:** commit nos últimos 6 meses, issues respondidas, não arquivado.
3. **Segurança e cadeia de suprimentos:** o que executa (binários, hooks, `postinstall`), que permissões pede, de onde baixa; fixar versão ou commit; nunca dar tokens além do necessário. **Revisar o texto e os scripts** da skill como se fosse código de biblioteca (prompt injection, exfiltração, rede, shell).
4. **Custo em tokens:** skills e regras longas consomem contexto. Preferir as que carregam sob demanda.
5. **Encaixe:** resolve algo de um fluxo ou de um papel e não duplica recurso já adotado.
6. **Dados:** nada que envie código ou dados de cliente a terceiros sem aprovação (LGPD).

### 3.1 Skills de comunidade e marketplaces
- **Tratar skill de comunidade como biblioteca:** mesma avaliação de licença, manutenção e revisão de scripts/instruções; só depois copiar a **versão revisada** (commit fixo) para o repositório em `.cursor/skills/`. Não symlinks vivos para pastas externas sem pin.
- **Marketplaces MCP remotos de skills** (Agensi e qualquer outro que carregue `SKILL.md` sob demanda via MCP, sem arquivo versionado no repo): **descartados por enquanto**. Motivos: o conteúdo pode mudar sem o agente ver o diff; risco de injeção em instruções servidas em tempo real; muitos itens são pagos (custo → Samuel). Preferir descobrir pelo git/`skills.sh` e instalar cópia revisada no repo.
- Diretórios/índices que só apontam para repositórios públicos (ex.: skills.sh) podem servir à **descoberta**, desde que a adoção siga o fluxo acima (clonar/pin → revisar → copiar para `.cursor/skills/`).

### 3.2 Coleções de comunidade em avaliação (18/10/2026)
Ambas MIT, só instruções em Markdown, **status: em avaliação**. Revisão dos `SKILL.md` da shortlist: sem chamadas de rede, sem git destrutivo e sem serviço pago. **Ainda não copiadas** para `.cursor/skills/`; detalhes e riscos em `recursos.yaml`.

| Coleção | Pin | Shortlist | Fora | Atenções da revisão |
|---|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) (~296 mil estrelas, 38 skills) — processo | `49dd158` | grill-with-docs, to-questionnaire, to-spec, to-tickets, wayfinder, tdd, diagnosing-bugs, code-review, pr, domain-modeling, research, handoff, writing-for-agents | Específicas do Claude Code, de TypeScript/cursos e `in-progress/` | grill-with-docs depende de `grilling`; to-spec/to-tickets/wayfinder/code-review pressupõem `/setup-matt-pocock-skills` e **publicam no issue tracker** (ação externa → usar backlog/tracker local); research e code-review abrem subagentes (só locais, sem agentes de nuvem); diagnosing-bugs traz script bash interativo (fora do TT-060); handoff grava em `/tmp`; termos do Claude Code a adaptar |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) (~47 mil estrelas, 15 skills) — só frontend/design | `2d22863` | emil-design-eng, apple-design, pick-ui-library, break-ui, mobile-native, animate-expo, animate, review-animations, improve-animations, animation-performance | write-swift, ask-sonner | **Comparar com o impeccable antes de adotar** (evitar regras de design conflitantes); animate-expo/pick-ui-library instalam dependências (só com pedido, conferir licença); emil-design-eng é longa (~670 linhas, carregar sob demanda) |

Decide: o papel responsável junto com o Arquiteto, registrando em `recursos.yaml`. **Vai para o Samuel** o que tiver custo, conta nova, envio de dados a terceiros ou licença duvidosa.

### 3.3 Memória, contexto e economia de tokens (21/10/2026)
Sugestões do Samuel. Nada instalado nem executado; detalhes em `recursos.yaml`.

| Projeto | Pin | Licença | Decisão | O que extrair |
|---|---|---|---|---|
| [kingbootoshi/cartographer](https://github.com/kingbootoshi/cartographer) | `a62d169` | sem licença | em avaliação (só ideia) | Mapa de codebase (`docs/CODEBASE_MAP.md`) por projeto, atualizado por incremento — VTX-131 |
| [centminmod/my-claude-code-setup](https://github.com/centminmod/my-claude-code-setup) | `7d5c374` | MIT | adaptar | Memory bank em arquivos (padrões, decisões, troubleshooting, contexto ativo) no formato AGENTS.md/.cursor/rules — VTX-132 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | `bbb3379` | Apache-2.0 | descartar | Só o padrão de observações tipadas e datadas (entra no VTX-132); serviço hospedado por padrão e hooks |
| [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | `4c7acba` | Apache-2.0 | em avaliação | Regras de compressão de saída de ferramentas e logs — VTX-133; piloto local do MCP com telemetria desligada |

### 3.4 Personas de agentes e integração (21/10/2026)
Nada instalado nem executado; detalhes em `recursos.yaml`.

| Projeto | Pin | Licença | Decisão | O que extrair |
|---|---|---|---|---|
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (~163 mil estrelas) | `4e3ac3c` | MIT | adaptar | Processo, entregáveis e métricas por persona para enriquecer os papéis de `papeis-de-agentes.md`; novos especialistas sob demanda (mudança mínima, onboarding de codebase, fluxo git, resposta a incidentes) — VTX-134 |
| [trailhq/Trail-Code](https://github.com/trailhq/Trail-Code) (antigo graft, ~10,6 mil estrelas) | `b1211ef` | MIT | em avaliação | Mapa de código local (tree-sitter, sem rede) via MCP/CLI e aprendizados versionados em `.trail/` (decisão/preferência/guardrail); piloto local com telemetria desligada, sem `init`, `--deep` nem workspace — VTX-135. Corrige a identificação anterior (graftcode) |

### 3.5 Melhoria contínua de skills (21/10/2026)
Nada instalado nem executado; detalhes em `recursos.yaml`.

| Projeto | Pin | Licença | Decisão | O que extrair |
|---|---|---|---|---|
| [rebelytics/one-skill-to-rule-them-all](https://github.com/rebelytics/one-skill-to-rule-them-all) — skill `task-observer` (~3,5 mil estrelas) | `3463c7c` | CC-BY-4.0 | adaptar | Log de observações por skill (padrões, correções, julgamentos) com checkpoints e revisão periódica que vira proposta de atualização de skill — VTX-136. Nome ambíguo: "task observer" é o nome da skill, não do repo (alternativas em `recursos.yaml`) |
| [google-research/harness2](https://github.com/google-research/harness2) (~17 mil estrelas) | `1cfe254` | Apache-2.0 | adaptar só a metodologia | Ciclo Propose–Probe–Compose para mudar regras/skills (propor, testar numa tarefa real, comparar, adotar) e registro de lições com evidência; mapa dos 8 componentes do harness para o Cursor (rules, AGENTS.md, memory bank, MCP, skills, scripts, papéis) — VTX-137. Não executar: exige modelos pagos e rede irrestrita |

### 3.6 ECC — Everything Claude Code (21/10/2026)
[affaan-m/ECC](https://github.com/affaan-m/ECC), MIT, ~286 mil estrelas, pin `90606c8`. **Decisão: adaptar por partes**, sem instalar o pacote. Inventário completo e riscos em `recursos.yaml`.

| Categoria (qtd.) | Já temos/planejado | Vira no Cursor (VTX) |
|---|---|---|
| Rules (23 pastas: common + linguagens) | `padroes-de-codigo.md`, regras por assunto (VTX-057/058) | `.cursor/rules/` comuns (estilo, testes, segurança, git, performance) e por stack (typescript, react, react-native, python), reescritas em pt-BR — **VTX-138** |
| Hooks (`.cursor/hooks.json`) | nada | Hooks mínimos do Cursor: `beforeShellExecution` (bloquear `--no-verify`, push forçado, segredos), `beforeReadFile` (.env), `afterFileEdit` (formatador) + script do arsenal TT-060 — **VTX-139** |
| Skills (311) | mattpocock, emilkowalski, impeccable, superpowers | Só lacunas do stack: verification-loop, tdd-workflow, search-first, strategic-compact/context-budget, security-review, e2e-testing, api-design/contract-first, postgres-patterns, deployment-patterns, mcp-dependency-review em `.cursor/skills/` — **VTX-140** |
| Agents (71) | `papeis-de-agentes.md` + VTX-134 | Não importar; usar como fonte extra no VTX-134 |
| Commands (97) | fluxos em `knowledge/processos/` | Não importar; plan-prd/feature-dev/quality-gate só como referência dos fluxos |
| Memória, aprendizado, codemaps | VTX-131/132/135/136/137 | Ignorar (já coberto) |
| MCP configs (~35) | Playwright, Context7, GitHub | Nada novo grátis/local além dos já avaliados |

## 4. Registro (`recursos.yaml`)
Campos: `id`, `nome`, `area`, `tipo` (skill | regras | mcp | componentes | referência | lista), `link`, `licenca`, `status` (em avaliação | adotado | descartado), `uso_agentes`, `riscos`, `responsavel` (papel de `agents/`), `revisado_em`. O CI valida os campos (teste `tests/test_recursos.py`). Um item descartado continua no registro com o motivo, para não ser reavaliado à toa.

## 5. Como os agentes encontram e usam
- Cada definição em [`agents/`](../../agents/README.md) ganha a seção "Recursos" filtrada pela `area` do papel (VTX-128). Os fluxos citam os recursos adotados na etapa em que eles entram.
- Os recursos adotados viram skills e regras do Cursor na F9/F10. Skills de comunidade aprovadas entram como cópia revisada em `.cursor/skills/` do repositório (não via MCP remoto). O formato e os exportadores seguem o tek-team (VTX-082): a VTX registra o que usar, e o tek-team define como empacotar, sem duplicar.
- A plataforma de acompanhamento (F11) pode exibir o registro mais adiante.

## Fontes
- READMEs dos repositórios citados, consultados em 17/10/2026 (licença e atividade pela API do GitHub).
- OpenSSF, *Concise Guide for Evaluating Open Source Software*: critérios de manutenção e cadeia de suprimentos.
