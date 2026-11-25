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
1. **Licença** (vale para código **copiado para entregas de clientes**; para uso interno da VTX, ver o princípio em [radar.md](radar.md)): MIT, Apache-2.0, BSD e CC0 são aceitas. CC-BY e CC-BY-SA só para referência, com atribuição. Sem licença ou com licença restritiva: não copiar. Em repositórios mistos (ex.: anthropics/skills), conferir a licença **de cada skill** — as de documento (`docx`, `pdf`, `pptx`, `xlsx`) são source-available sob termos da Anthropic, **não** open source: não copiar.
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
| [kingbootoshi/cartographer](https://github.com/kingbootoshi/cartographer) | `a62d169` | sem licença | só ideia (padrão VTX publicado) | A ferramenta continua fora (sem licença). O padrão original está em [mapa-de-codebase.md](../engenharia/mapa-de-codebase.md) — VTX-131 |
| [centminmod/my-claude-code-setup](https://github.com/centminmod/my-claude-code-setup) | `7d5c374` | MIT | adaptado | Templates em [memoria-projeto/](../templates/memoria-projeto/README.md), escritos do zero em pt-BR; nenhum trecho copiado; sem hooks — VTX-132 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | `bbb3379` | Apache-2.0 | descartado | Só o padrão de observações tipadas (`decision`, `bugfix`, `security_alert`) entrou no memory bank; serviço e hooks ficam fora |
| [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | `4c7acba` | Apache-2.0 | em avaliação | Regras de compressão de saída de ferramentas e logs — VTX-133; piloto local do MCP com telemetria desligada |

### 3.4 Personas de agentes e integração (21/10/2026)
Nada instalado nem executado; detalhes em `recursos.yaml`.

| Projeto | Pin | Licença | Decisão | O que extrair |
|---|---|---|---|---|
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (~163 mil estrelas) | `4e3ac3c` | MIT | adaptar | Processo, entregáveis e métricas por persona para enriquecer os papéis de `papeis-de-agentes.md`; novos especialistas sob demanda (mudança mínima, onboarding de codebase, fluxo git, resposta a incidentes) — VTX-134 |
| [trailhq/Trail-Code](https://github.com/trailhq/Trail-Code) (antigo graft, ~10,6 mil estrelas) | `b1211ef` | MIT | **adotado** com restrições (VTX-135) | Mapa local (`graft` 0.23.1: `build`/`ask`/`skeleton`/`check`) no [sandbox](../../projects/sandbox-trail-code/); sem `init`, `--deep`, workspace, upgrade ou MCP no vtx-core. Relato em [piloto-trail-code.md](piloto-trail-code.md). |

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

### 3.7 diagram-design — diagramas editoriais (21/10/2026, adaptação 24/11/2026)
[cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design), MIT, ~60 mil estrelas, pin `7a12007` (`7a12007b5a4246894f342a2e52e78facbc62eca3`). Skill de 45 tipos de diagrama em HTML + SVG autocontido (sem Mermaid), com tema de marca. Sem servidor, sem telemetria (PRIVACY.md); único acesso externo no original é Google Fonts. **Decisão: adaptar** — feita na VTX-141.
- Skill no Cursor: [`.cursor/skills/diagramas/`](../../.cursor/skills/diagramas/) (SKILL.md em pt-BR, `tema-vtx.css`, 3 templates; atribuição e pin em `NOTICE.md`). Fontes locais (`system-ui` / Segoe UI / Liberation). Sem Google Fonts, sem scripts do repo de origem, sem os 45 `type-*.md`.
- Tema VTX provisório (petróleo `#0f5c6b` no papel `#f4f1ea`) até haver marca oficial. PNG, se precisar, com o Playwright já adotado.
- Uso: ADRs, arquitetura e fluxos em `docs/` (primeiro lote: [diagramas dos ADRs do med-hub](../../projects/med-hub/docs/adr/diagramas/)), README e sites.

### 3.8 HyperFrames (HeyGen) — vídeo a partir de HTML (21/10/2026)
[heygen-com/hyperframes](https://github.com/heygen-com/hyperframes), Apache-2.0, ~69 mil estrelas, pin `4371981`. Agentes escrevem HTML e o CLI renderiza MP4 local (Chrome headless + FFmpeg, Node 22+). **Decisão: adaptar, com cuidado.**
- Riscos: CLI tem **telemetria ligada por padrão** (desligar com `HYPERFRAMES_NO_TELEMETRY=1`/`DO_NOT_TRACK=1`); há render em nuvem (AWS Lambda/GCP), registry remoto e instaladores `npx` — tudo fora. Só render local; instalar apenas após revisão, em ambiente isolado.
- Vira no Cursor: skill `.cursor/skills/video-marketing/` adaptada das skills core (`hyperframes`, `hyperframes-cli`), script do arsenal TT-060 `render-video` (render local com telemetria desligada) e a ideia do `frame.md` (design.md traduzido para vídeo) como processo de marketing — **VTX-142**.
- Uso: vídeos curtos de divulgação e demos dos sites (site-vtx, site-med-hub, site-tekto). Prioridade baixa: depois dos sites existirem.

### 3.9 Serviços de cliente: Figma, Vercel, Supabase e Stripe (23/10/2026)
Pedido do Samuel: conectou Figma, Vercel e Supabase como conectores (MCP) e definiu o **Stripe como ferramenta principal de pagamento**. Não são plataformas pagas de agentes: são serviços dos projetos, com plano gratuito. Custos registrados com honestidade; valores marcados [A CONFIRMAR] antes de cada uso.
- **Figma** — handoff de design dos sites (site-vtx, site-med-hub, site-tekto) e das telas de produto. MCP oficial (Dev Mode) lê frames, variáveis e componentes para o agente gerar código. Plano Starter grátis tem limite baixo de chamadas MCP e Dev Mode é recurso pago [A CONFIRMAR]. Vira no Cursor: MCP (só leitura) + passo no fluxo `site-landing-page` (design.md ← tokens do Figma) — **VTX-110**.
- **Vercel** — hospedagem e preview por PR de sites Next.js. **Plano Hobby é grátis mas proíbe uso comercial**: serve para sites internos/não comerciais (painel, protótipos). Site comercial ou de cliente exige Pro (pago, por membro/mês) ou alternativa grátis (Cloudflare Pages, GitHub Pages). **Decisão de dinheiro do Samuel — não decidido.** Vira no Cursor: MCP (deploy/logs) + guia — **VTX-099**; afeta a ADR de hospedagem (VTX-096/F11).
- **Supabase** — backend (Postgres, auth, storage). Free: 2 projetos, ~500 MB de banco, pausa após 1 semana parado [A CONFIRMAR]; sem uso em produção com clientes (ver ADR-0002 do med-hub, aceito em 24/10/2026 com a VTX-023). Vira no Cursor: MCP **apontado só para projeto de desenvolvimento**, nunca produção, em modo somente leitura quando possível — **VTX-100**.
- **Stripe** — gateway de pagamento **principal** (Mercado Pago vira alternativa). Sem mensalidade; cobra taxa por transação [A CONFIRMAR taxas BR]; modo de teste grátis. Brasil: conta BR com cartão, boleto e Pix [A CONFIRMAR disponibilidade e taxas]. MCP oficial / Agent Toolkit só com **chave de teste restrita**. Padrão em `knowledge/engenharia/pagamentos.md` — **VTX-106**.
- Segurança: chaves (Stripe, Supabase service_role, tokens Vercel/Figma) nunca no repo nem no chat; manifestos registram só onde a chave está. Webhooks sempre com verificação de assinatura.

### 3.10 Frontend, UI e design (24/11/2026)
Pesquisa VTX-120. Nada novo instalado. Pins e licenças pela API do GitHub / páginas oficiais em 24/11/2026.

| Recurso | Pin / fonte | Licença | Decisão | O que fazer |
|---|---|---|---|---|
| [shadcn/ui](https://github.com/shadcn-ui/ui) (~129 mil estrelas) | `055aa6b` | MIT | **adotado** (já era padrão no VTX-023) | Componentes copiados, base Radix; manter aviso MIT |
| [Tailwind CSS](https://github.com/tailwindlabs/tailwindcss) (~99 mil estrelas) | `f646ff8` | MIT | **adotado** (VTX-023) | Tokens e utilitários; sem plugin pago |
| [Radix Primitives](https://github.com/radix-ui/primitives) (~20 mil estrelas) | `eb3a2b7` | MIT | **adotado** (base do shadcn) | Não trocar a base sem ADR |
| [axe-core](https://github.com/dequelabs/axe-core) (~8 mil estrelas) + `@axe-core/playwright` | `32d9bd5` | MPL-2.0 | **adotado** (VTX-023 / VTX-028) | Dependência npm, não copiar código; zero violação séria + teclado manual |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) nível AA | recomendação W3C | W3C Document License | **adotado** | Citar e resumir; alvo AA do stack |
| [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/) | `f14b249` (repo) | W3C Document License | **adotado** | Padrões de widget quando o shadcn/Radix não cobrir |
| [Impeccable](https://github.com/pbakaus/impeccable) (~116 mil estrelas, 62 regras, engine 0.1.27; npm 4.10.0 no pin, ponta 4.11.0 em 24/11) | `b49177d` | Apache-2.0 | **adotado** com restrições (VTX-127) | Detector + skill sob demanda; sem `npx install`, hooks, login ou Pro. Piloto em [projects/sandbox-impeccable/](../../projects/sandbox-impeccable/) |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | `2d22863` | MIT | em avaliação | Sem mudança; comparar com o impeccable antes de adotar |
| [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y) (~3,6 mil estrelas) | `8f75961` | MIT | em avaliação | Lint estático que complementa o axe; último commit em jan/2026 (fora da janela de 6 meses) |
| [React Aria](https://github.com/adobe/react-spectrum) (~16 mil estrelas) | `b1e8cf5` | Apache-2.0 | em avaliação | Alternativa à base Radix; **não misturar** na mesma tela |

Fora: Pa11y e HTML CodeSniffer (outro motor — resultados divergem do axe); produtos pagos da Deque. Cult UI e KokonutUI permanecem no [radar](radar.md), não neste registro.

### 3.11 Backend e APIs (24/11/2026)
Pesquisa VTX-121. Nada novo instalado. Pins e licenças pela API do GitHub / páginas oficiais em 24/11/2026.

| Recurso | Pin / fonte | Licença | Decisão | O que fazer |
|---|---|---|---|---|
| [Zod](https://github.com/colinhacks/zod) (~44 mil estrelas) | `d40c329` | MIT | **adotado** (VTX-023 / VTX-024) | Validação na borda; contrato antes do código |
| [supabase-js](https://github.com/supabase/supabase-js) (~4,6 mil estrelas) | `840843d` | MIT | **adotado** (VTX-023 / VTX-100) | Dados com RLS; `service_role` só no servidor |
| [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0) | `4f86429` (repo OAI) | Apache-2.0 | **adotado** | Contrato versionado, gerado a partir do Zod |
| [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) Problem Details | RFC | IETF Trust | **adotado** | Erros `application/problem+json` |
| [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines) | `1c58ca7` | CC-BY-4.0 | **adotado** | Citar e resumir, com atribuição |
| [pino](https://github.com/pinojs/pino) (~18 mil estrelas) | `b5fac26` | MIT | **adotado** (VTX-023) | Logs JSON com `trace_id`; sem PII |
| [zod-openapi](https://github.com/samchungy/zod-openapi) (~650 estrelas) | `4ae5375` | MIT | em avaliação | Gerar OpenAPI a partir do Zod; conferir a major |
| [openapi-typescript](https://github.com/openapi-ts/openapi-typescript) (~8 mil estrelas) | `d46a319` | MIT | em avaliação | Tipos a partir do contrato; não substitui o Zod |
| [Drizzle ORM](https://github.com/drizzle-team/drizzle-orm) (~36 mil estrelas) | `3bcb6a2` | Apache-2.0 | em avaliação | Só com ADR, quando o Postgres não for o Supabase |
| [Hono](https://github.com/honojs/hono) (~33 mil estrelas) | `9c2f294` | MIT | em avaliação | Alternativa ao Route Handler, só com ADR |

Fora: Prisma (o stack já escolheu supabase-js / Drizzle), tRPC e GraphQL (só com ADR, VTX-024), OpenAPI Generator (Java, pesado demais para o fluxo da VTX).

### 3.12 Testes e QA (24/11/2026)
Pesquisa VTX-122. Nada novo instalado. Pins e licenças pela API do GitHub em 24/11/2026.

| Recurso | Pin / fonte | Licença | Decisão | O que fazer |
|---|---|---|---|---|
| [Playwright](https://github.com/microsoft/playwright) (~101 mil estrelas) | `0caa804` | Apache-2.0 | **adotado** (VTX-018 / VTX-023) | E2E dos fluxos críticos + axe-core |
| [Vitest](https://github.com/vitest-dev/vitest) (~17 mil estrelas) | `e0e8e00` | MIT | **adotado** | Unidade/integração TS; TDD na regra de negócio |
| [Testing Library](https://github.com/testing-library/react-testing-library) (~20 mil estrelas) | `20ce75f` | MIT | **adotado** | Queries pela papel/acessível |
| [pytest](https://github.com/pytest-dev/pytest) (~15 mil estrelas) | `02576a5` | MIT | **adotado** | Só no Python (arsenal, IFC); não no app TS |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) (~40 mil estrelas) | `2337aff` | Apache-2.0 | em avaliação | Piloto só em ambiente de teste; não substitui o E2E da CI |

Fora: Cypress (o stack já escolheu Playwright). axe-core já entrou na VTX-120.

### 3.13 Segurança, cadeia de suprimentos e checklist de skill/hook (24/11/2026)
Pesquisa VTX-123. Nada novo instalado.

| Recurso | Pin / fonte | Licença | Decisão | O que fazer |
|---|---|---|---|---|
| [gitleaks](https://github.com/gitleaks/gitleaks) (~31 mil estrelas) | `5f6ec56` | MIT | **adotado** (VTX-023) | Segredos no CI, action pinada por SHA |
| [Semgrep CE](https://github.com/semgrep/semgrep) (~18 mil estrelas) | `c4dbe9e` | LGPL-2.1 | **adotado** | Só a Community Edition, local/CI; cloud pago está fora |
| [OSV-Scanner](https://github.com/google/osv-scanner) (~12 mil estrelas) | `66586f4` | Apache-2.0 | **adotado** | CVE no lockfile; PR sem alta/crítica |
| [OWASP Cheat Sheet Series](https://github.com/OWASP/CheatSheetSeries) (~34 mil estrelas) | `18e6c89` | CC-BY-SA-4.0 | **adotado** (já estava) | Citar e resumir, com atribuição |
| [Trivy](https://github.com/aquasecurity/trivy) (~40 mil estrelas) | `c14584a` | Apache-2.0 | em avaliação | Imagem/IaC quando houver Dockerfile; sem SaaS pago |
| [ZAP](https://github.com/zaproxy/zaproxy) (~16 mil estrelas) | `11a4557` | Apache-2.0 | em avaliação | Baseline só em homologação |

Fora: CodeQL em repositório privado (pode exigir GitHub Advanced Security, pago → A2); Semgrep Code/Secrets/Cloud; scanners SaaS pagos.

**Checklist — revisar skill, hook ou `npx` de comunidade antes de instalar:**
1. Licença aceita (§3) e commit/pin fixos; repositório não arquivado.
2. Ler o `SKILL.md` **e** os scripts por completo, não só o README.
3. Procurar rede (`curl`, `wget`, `fetch`, telemetria), `postinstall`, hooks, shell, leitura de `.env`/tokens, git destrutivo (`push --force`, `reset --hard`) e instruções de exfiltração ou de ignorar estas regras.
4. Permissões = mínimo da tarefa; nenhum token além do necessário.
5. Se houver binário, hook ou download no primeiro uso: só depois de piloto em sandbox (como o impeccable, VTX-127).
6. Copiar a versão revisada para `.cursor/skills/` do repo, com pin e atribuição; sem symlink vivo nem marketplace MCP remoto de skills (§3.1).
7. Custo, conta nova, envio de código/dados a terceiros ou licença duvidosa → pedido A2 ao Samuel; silêncio não aprova.

### 3.14 Documentação (24/11/2026)
Pesquisa VTX-124. Nada instalado. A escolha do gerador padrão fica para a VTX-032 (docs-as-code). Pins e licenças pela API do GitHub / LICENSE em 24/11/2026.

| Recurso | Pin / fonte | Licença | Decisão | O que fazer |
|---|---|---|---|---|
| [Diátaxis](https://github.com/evildmp/diataxis-documentation-framework) | `957c09c` · [diataxis.fr](https://diataxis.fr/) | CC-BY-SA-4.0 | em avaliação | Inspiração de tipos de doc; citar com atribuição; não trocar o formato do INDEX ad hoc |
| [Astro Starlight](https://github.com/withastro/starlight) (~9,6 mil estrelas) | `80f3055` | MIT | em avaliação | Candidato principal (casa com a alternativa Astro do stack) |
| [Docusaurus](https://github.com/facebook/docusaurus) (~67 mil estrelas) | `809ffff` | MIT | em avaliação | Alternativa React/MDX, só com ADR |
| [VitePress](https://github.com/vuejs/vitepress) (~18 mil estrelas) | `40b2e09` | MIT | em avaliação | Stack Vue, só com ADR |
| [TypeDoc](https://github.com/TypeStrong/typedoc) (~8,5 mil estrelas) | `6d8c856` | Apache-2.0 | em avaliação | Referência de API TS, complementar |
| [Vale](https://github.com/errata-ai/vale) (~6,4 mil estrelas) | `7498767` | MIT | em avaliação | Linter de prosa local, depois da VTX-032 |
| [Mermaid](https://github.com/mermaid-js/mermaid) (~91 mil estrelas) | `6374e52` | MIT | em avaliação | Rascunho em Markdown; diagramas editoriais ficam com a VTX-141 |

Fora: Mintlify e Material for MkDocs Insiders (pagos). OpenAPI já entrou na VTX-121.

### 3.15 Skills de agentes e regras do Cursor (24/11/2026)
Pesquisa VTX-125. Nada novo copiado para `.cursor/skills/`.

**Fronteira com o tek-team (VTX-082):** a VTX **registra o que usar** neste YAML e nas cópias revisadas em `.cursor/skills/`. O **formato-fonte e os exportadores** de agentes são do [tek-team](https://github.com/SamAlencar/tek-team) (TT-096 e TT-100 a TT-103). Não duplicar isso em `agentes/`. A VTX-082 continua à espera do Tek.

| Recurso | Pin / fonte | Licença | Decisão | O que fazer |
|---|---|---|---|---|
| [Superpowers — verification-before-completion](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/verification-before-completion) | `bb92a777` (já no repo) | MIT | **adotado** | Já usada em toda tarefa; faltava no registro. Pin local não sobe para `22f0b46` sem revisão da cópia |
| Superpowers writing-plans e brainstorming | `bb92a777` | MIT | **adotado** (já estavam) | Sem mudança de pin |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) (~35 mil estrelas) | ativa em 20/11 | licença não declarada | em avaliação | Sem LICENSE na raiz — não copiar |
| [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) (~41 mil estrelas) | `b044f95` (30/05/2026) | CC0-1.0 | em avaliação | Só ideias; no limite da janela de 6 meses |

O restante do catálogo de skills (mattpocock, ECC, impeccable, etc.) permanece como já registrado nas seções 3.2–3.9. Instalação continua sujeita ao checklist da §3.13.

### 3.16 Servidores MCP (24/11/2026)
Pesquisa VTX-126. Fontes: Registry oficial e listas. Regra: **só leitura e escopo mínimo**. Nada novo instalado além do que Samuel já conectou (GitHub, Figma, Vercel, Supabase).

| Recurso | Pin / fonte | Licença | Decisão | O que fazer |
|---|---|---|---|---|
| [MCP Registry](https://registry.modelcontextprotocol.io) | `0c74fa6` (repo) | Apache-2.0 (transição MIT) | **adotado** (descoberta) | Fonte primária; listing não é auditoria |
| [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) (~98 mil estrelas) | `ac5cc37` | MIT | em avaliação | Só descoberta complementar |
| [GitHub MCP](https://github.com/github/github-mcp-server) (~35 mil estrelas) | `c6b6295` | MIT | **adotado** | Já em uso; token de escopo mínimo |
| [Supabase MCP](https://github.com/supabase/mcp) (~3 mil estrelas) | `56093a6` | Apache-2.0 | **adotado** | Só projeto `dev`, `read_only=true`; nunca produção |
| [Figma MCP](https://developers.figma.com/docs/figma-mcp-server/) | `5e47908` (guia) | serviço oficial | **adotado** | Só handoff de leitura; cota do Starter; sem escrita no canvas |
| [Vercel MCP](https://vercel.com/docs/agent-resources/vercel-mcp) | `https://mcp.vercel.com` | serviço oficial | **adotado** | Ler deploy/log; produção só pelo Git |
| [Reference servers](https://github.com/modelcontextprotocol/servers) (filesystem / fetch) | `c799c85` | Apache-2.0 (transição MIT) | em avaliação | Filesystem só com `--read-only` e diretórios explícitos |
| [Stripe AI / MCP](https://github.com/stripe/ai) (~2 mil estrelas) | `f10dc33` | MIT | em avaliação | Só chave de teste restrita |

Sem mudança de status: Playwright MCP (piloto em teste, VTX-122), Headroom (VTX-133). Trail-code passou a **adotado com restrições** (VTX-135; [piloto-trail-code.md](piloto-trail-code.md)). Agensi e qualquer marketplace remoto de skills continuam **descartados** (§3.1).

**Regra de conexão:** servidor do catálogo + leitura (ou `--read_only` / `read_only=true`) + o menor token/projeto possível. Conteúdo lido por MCP é não confiável. Custo, conta nova ou escrita em produção → A2.

## 4. Registro (`recursos.yaml`)
Campos: `id`, `nome`, `area`, `tipo` (skill | regras | mcp | componentes | referência | lista), `link`, `licenca`, `status` (em avaliação | adotado | descartado), `uso_agentes`, `riscos`, `responsavel` (papel de `agents/`), `revisado_em`. O CI valida os campos (teste `tests/test_recursos.py`). Um item descartado continua no registro com o motivo, para não ser reavaliado à toa.

## 5. Como os agentes encontram e usam
- Cada definição em [`agents/`](../../agents/README.md) ganha a seção "Recursos" filtrada pela `area` do papel (VTX-128). Os fluxos citam os recursos adotados na etapa em que eles entram.
- Os recursos adotados viram skills e regras do Cursor na F9/F10. Skills de comunidade aprovadas entram como cópia revisada em `.cursor/skills/` do repositório (não via MCP remoto). O formato e os exportadores seguem o tek-team (VTX-082): a VTX registra o que usar, e o tek-team define como empacotar, sem duplicar.
- A plataforma de acompanhamento (F11) pode exibir o registro mais adiante.

## Fontes
- READMEs dos repositórios citados, consultados em 17/10/2026 (licença e atividade pela API do GitHub).
- OpenSSF, *Concise Guide for Evaluating Open Source Software*: critérios de manutenção e cadeia de suprimentos.
