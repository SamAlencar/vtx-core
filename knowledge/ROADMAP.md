# Roadmap da Base de Conhecimento

Gerado por `scripts/gerar_roadmap.py` a partir de `backlog/projeto.yaml` (fonte da verdade).
Uma tarefa por sessão diária, em ordem de prioridade. Próxima: `python scripts/proxima_tarefa.py`.
Ao concluir um documento, adicioná-lo ao `INDEX.md`.


## F1 — Processo e operação de agentes

1. **VTX-010** Fluxo de trabalho entre agentes (SOP) → `knowledge/processos/fluxo-entre-agentes.md`
2. **VTX-066** Guia de classificação e triagem de projetos (inclui híbridos) → `knowledge/processos/fluxos/triagem.md`
3. **VTX-067** Fluxo de projeto: sistema web / plataforma SaaS → `knowledge/processos/fluxos/sistema-web-saas.md`
4. **VTX-068** Fluxo de projeto: app mobile → `knowledge/processos/fluxos/app-mobile.md`
5. **VTX-069** Fluxo de projeto: API e integrações → `knowledge/processos/fluxos/api-integracoes.md`
6. **VTX-070** Fluxo de projeto: site / landing page → `knowledge/processos/fluxos/site-landing-page.md`
7. **VTX-071** Fluxo de projeto: manutenção e evolução de sistema existente → `knowledge/processos/fluxos/manutencao-evolucao.md`
8. **VTX-084** Fluxo de entrevista com o cliente (descoberta) → `knowledge/processos/fluxos/entrevista-cliente.md`
9. **VTX-130** Pesquisa de domínio e base de conhecimento do projeto do cliente → `knowledge/processos/pesquisa-de-dominio.md`
10. **VTX-072** Fluxo de projeto: MVP / prova de conceito → `knowledge/processos/fluxos/mvp-poc.md`
11. **VTX-011** Engenharia de requisitos → `knowledge/processos/engenharia-de-requisitos.md`
12. **VTX-012** Scrum e Kanban adaptados a agentes → `knowledge/processos/scrum-kanban-agentes.md`
13. **VTX-013** Operação de agentes: prompts, contexto e memória → `knowledge/processos/operacao-de-agentes.md`
14. **VTX-014** Governança e aprovações (humano no circuito) → `knowledge/processos/governanca-e-aprovacoes.md`

## F2 — Engenharia de software

15. **VTX-015** Arquitetura de software (estilos, C4, ADRs) → `knowledge/engenharia/arquitetura-de-software.md`
16. **VTX-016** Padrões de projeto e DDD → `knowledge/engenharia/padroes-de-projeto-ddd.md`
17. **VTX-017** Padrões de código, Clean Code e code review → `knowledge/engenharia/padroes-de-codigo.md`
18. **VTX-018** Estratégia de testes e qualidade → `knowledge/engenharia/testes-e-qualidade.md`
19. **VTX-019** Git e CI/CD → `knowledge/engenharia/git-e-ci-cd.md`

## F3 — Segurança e operação

20. **VTX-020** Segurança no desenvolvimento (OWASP, SSDF) → `knowledge/seguranca/desenvolvimento-seguro.md`
21. **VTX-021** DevOps e SRE (IaC, SLOs, incidentes) → `knowledge/operacao/devops-sre.md`
22. **VTX-022** Observabilidade (logs, métricas, traces) → `knowledge/operacao/observabilidade.md`

## F4 — Tecnologia e plataformas

23. **VTX-023** Stack de referência da VTX → `knowledge/tecnologia/stack-de-referencia.md`
24. **VTX-024** Design de APIs → `knowledge/tecnologia/design-de-apis.md`
25. **VTX-025** Modelagem de dados e bancos de dados → `knowledge/tecnologia/modelagem-de-dados.md`
26. **VTX-026** Desenvolvimento frontend web → `knowledge/tecnologia/frontend-web.md`
27. **VTX-027** Desenvolvimento mobile → `knowledge/tecnologia/mobile.md`
28. **VTX-028** UX/UI e acessibilidade → `knowledge/tecnologia/ux-ui-acessibilidade.md`

## F12 — Catálogo de ferramentas

29. **VTX-098** Base do catálogo de ferramentas (estrutura, modelo, critérios, matriz) → `knowledge/ferramentas/README.md`
30. **VTX-099** Ferramenta: Vercel → `knowledge/ferramentas/hospedagem/vercel.md`
31. **VTX-100** Ferramenta: Supabase (banco, auth, storage) → `knowledge/ferramentas/backend/supabase.md`
32. **VTX-101** Ferramenta: GitHub e GitHub Actions → `knowledge/ferramentas/ci-cd/github-actions.md`
33. **VTX-102** Ferramenta: Cursor (regras, agentes locais e na nuvem) → `knowledge/ferramentas/ia-dev/cursor.md`
34. **VTX-142** Vídeos de divulgação com HyperFrames (render local) → `.cursor/skills/video-marketing/ + script do arsenal (TT-060) render-video + processo frame.md`
35. **VTX-103** Ferramenta: Appwrite → `knowledge/ferramentas/backend/appwrite.md`
36. **VTX-104** Ferramenta: Firebase → `knowledge/ferramentas/backend/firebase.md`
37. **VTX-105** Ferramenta: Expo e EAS → `knowledge/ferramentas/mobile/expo.md`
38. **VTX-106** Ferramentas de pagamento: Stripe e Mercado Pago → `knowledge/ferramentas/pagamentos/stripe-mercado-pago.md`
39. **VTX-107** Ferramenta: Sentry → `knowledge/ferramentas/observabilidade/sentry.md`
40. **VTX-108** Ferramenta: Cloudflare (DNS, Pages, Access, WAF) → `knowledge/ferramentas/ci-cd/cloudflare.md`
41. **VTX-109** Ferramenta: Docker → `knowledge/ferramentas/ci-cd/docker.md`
42. **VTX-110** Ferramenta: Figma → `knowledge/ferramentas/design/figma.md`
43. **VTX-111** Ferramentas de comunicação e gestão (Google Workspace, Grok Bot) → `knowledge/ferramentas/comunicacao/google-workspace.md`
44. **VTX-112** Matriz ferramenta × fluxo completa e links nos fluxos → `knowledge/ferramentas/README.md`
45. **VTX-113** Processo periódico de revisão de ferramentas → `knowledge/ferramentas/revisao-periodica.md`
46. **VTX-119** Bibliotecas e recursos para agentes: processo e registro → `knowledge/ferramentas/bibliotecas-e-recursos.md`
47. **VTX-120** Pesquisa de recursos: frontend, UI e design → `knowledge/ferramentas/recursos.yaml`
48. **VTX-121** Pesquisa de recursos: backend e APIs → `knowledge/ferramentas/recursos.yaml`
49. **VTX-122** Pesquisa de recursos: testes e QA → `knowledge/ferramentas/recursos.yaml`
50. **VTX-123** Pesquisa de recursos: segurança e cadeia de suprimentos → `knowledge/ferramentas/recursos.yaml`
51. **VTX-124** Pesquisa de recursos: documentação → `knowledge/ferramentas/recursos.yaml`
52. **VTX-125** Pesquisa de recursos: skills de agentes e regras do Cursor → `knowledge/ferramentas/recursos.yaml`
53. **VTX-126** Pesquisa de recursos: servidores MCP → `knowledge/ferramentas/recursos.yaml`
54. **VTX-127** Piloto do impeccable em uma tela de teste (fluxo frontend) → `projects/sandbox-impeccable/`

## F10 — Arsenal de scripts e papéis administrativos

55. **VTX-141** Skill de diagramas editoriais (adaptada do diagram-design) → `.cursor/skills/diagramas/ + diagramas dos ADRs do med-hub`

## F12 — Catálogo de ferramentas

56. **VTX-128** Integrar o registro de recursos às definições dos agentes e aos fluxos → `agents/ + knowledge/processos/fluxos/`
57. **VTX-129** Varredura periódica de recursos na manutenção quinzenal e revisão trimestral → `knowledge/ferramentas/revisao-periodica.md`
58. **VTX-131** Padrão de mapa de codebase por projeto (inspirado no Cartographer) → `knowledge/engenharia/mapa-de-codebase.md`
59. **VTX-132** Memory bank dos projetos em arquivos (adaptado de my-claude-code-setup e claude-mem) → `knowledge/templates/memoria-projeto/`
60. **VTX-133** Regras de economia de contexto em saídas de ferramentas e piloto local do Headroom → `.cursor/rules/economia-de-contexto.mdc`
61. **VTX-135** Piloto local do Trail-code (graft map) como ferramenta do mapa de codebase → `knowledge/ferramentas/piloto-trail-code.md`
62. **VTX-136** Observação contínua de skills e revisão na manutenção quinzenal (adaptado do task-observer) → `knowledge/processos/observacao-de-skills.md`
63. **VTX-137** Processo de melhoria do harness da VTX no Cursor (metodologia do Harness²) → `knowledge/processos/melhoria-do-harness.md`
64. **VTX-140** Skills do ECC que preenchem lacunas do stack VTX → `.cursor/skills/ (verification-loop, tdd-workflow, search-first, context-budget, security-review, e2e-testing, api-design, postgres-patterns, deployment-patterns, mcp-dependency-review)`

## F5 — Gestão e conformidade

65. **VTX-029** Gestão de projetos, riscos e comunicação com cliente → `knowledge/gestao/gestao-de-projetos.md`
66. **VTX-030** Estimativas e planejamento → `knowledge/gestao/estimativas.md`
67. **VTX-031** LGPD e compliance → `knowledge/seguranca/lgpd-compliance.md`
68. **VTX-032** Documentação técnica (docs-as-code) → `knowledge/gestao/documentacao-tecnica.md`

## F6 — Templates de artefatos

69. **VTX-033** Template de PRD → `knowledge/templates/prd.md`
70. **VTX-034** Template de história de usuário e critérios de aceite → `knowledge/templates/historia-de-usuario.md`
71. **VTX-035** Template de ADR → `knowledge/templates/adr.md`
72. **VTX-036** Template de plano e relatório de testes → `knowledge/templates/plano-de-testes.md`
73. **VTX-037** Template de runbook e postmortem → `knowledge/templates/runbook-postmortem.md`
74. **VTX-038** Template de relatório diário e de sprint → `knowledge/templates/relatorios.md`

## F7 — Diretrizes por papel

75. **VTX-039** Diretrizes do agente Orquestrador → `knowledge/diretrizes/orquestrador.md`
76. **VTX-040** Diretrizes do agente Produto → `knowledge/diretrizes/produto.md`
77. **VTX-041** Diretrizes do agente Arquiteto → `knowledge/diretrizes/arquiteto.md`
78. **VTX-042** Diretrizes do agente Dev Backend → `knowledge/diretrizes/dev-backend.md`
79. **VTX-043** Diretrizes do agente Dev Frontend/Mobile → `knowledge/diretrizes/dev-frontend-mobile.md`
80. **VTX-044** Diretrizes do agente QA → `knowledge/diretrizes/qa.md`
81. **VTX-045** Diretrizes do agente DevOps/SRE → `knowledge/diretrizes/devops-sre.md`
82. **VTX-046** Diretrizes dos especialistas sob demanda → `knowledge/diretrizes/especialistas.md`

## F9 — Integração com o Cursor e operação

83. **VTX-053** AGENTS.md raiz com diretrizes gerais dos agentes → `AGENTS.md`
84. **VTX-054** Regra sempre ativa: fluxo entre papéis, DoD e aprovações → `.cursor/rules/vtx-base.mdc`
85. **VTX-055** Regras por papel: Orquestrador, Produto e Arquiteto → `.cursor/rules/papeis/planejamento.mdc`
86. **VTX-056** Regras por papel: Devs, QA e DevOps/SRE → `.cursor/rules/papeis/execucao.mdc`
87. **VTX-134** Enriquecer papéis de agentes com o catálogo agency-agents → `knowledge/organizacao/papeis-de-agentes.md`
88. **VTX-057** Regras por assunto com globs: testes e APIs → `.cursor/rules/assuntos/testes-api.mdc`
89. **VTX-058** Regras por assunto com globs: frontend/mobile e segurança → `.cursor/rules/assuntos/frontend-seguranca.mdc`
90. **VTX-138** Regras comuns e por stack em .cursor/rules a partir do ECC → `.cursor/rules/ (common-*, typescript, react, react-native, python) e knowledge/templates/cursor/`
91. **VTX-139** Hooks do Cursor como guardrails locais (adaptados do ECC) → `.cursor/hooks.json e scripts/hooks/ (padrão TT-060)`
92. **VTX-059** Estratégia de consulta sob demanda e índice para agentes → `knowledge/index.yaml`
93. **VTX-060** Template de repositório de projeto → `templates/projeto/`
94. **VTX-061** Sincronização de regras e script de bootstrap de projetos → `scripts/bootstrap_projeto.sh`
95. **VTX-062** Ambiente dos agentes de nuvem (environment.json, segredos, permissões) → `.cursor/environment.json`
96. **VTX-063** Orquestração com issues, PRs e agentes de nuvem por papel e tipo de projeto → `knowledge/processos/orquestracao-cursor.md`
97. **VTX-064** Pontos de aprovação do Samuel (branch protegida, revisões, release) → `knowledge/processos/pontos-de-aprovacao.md`
98. **VTX-065** Teste de validação da integração com o Cursor → `projects/validacao-cursor/`

## F11 — Plataforma de acompanhamento (projeto interno)

99. **VTX-085** Planejamento da plataforma de acompanhamento → `knowledge/projetos-internos/plataforma-acompanhamento.md`
100. **VTX-114** Plataforma: revisão do plano (ferramentas, conexões, Cursor primeiro) → `knowledge/projetos-internos/plataforma-acompanhamento.md`
101. **VTX-086** Plataforma: PRD do MVP, hipóteses e critérios de sucesso → `vtx-acompanhamento/docs/prd-mvp.md`
102. **VTX-087** Formatos de registro: eventos, handoffs, decisões e custos → `registro/ + backlog/SCHEMA.md`
103. **VTX-088** Formato da fila de aprovações do Samuel → `registro/aprovacoes.yaml + backlog/SCHEMA.md`
104. **VTX-115** Esquema do manifesto de conexões por projeto → `projects/CONEXOES.md + projects/<p>/conexoes.yaml`
105. **VTX-089** Gerador de dados da plataforma (JSON privado único) → `vtx-acompanhamento/gerador/`

## F13 — Capacidades para o piloto plataforma-projetos

106. **VTX-143** Conhecimento de domínio BIM/IFC (IFC4/IFC4x3, IDS, openBIM) → `projects/plataforma-projetos/conhecimento/bim-ifc.md`
107. **VTX-144** Skill IFC no navegador (That Open Components e web-ifc) → `.cursor/skills/ifc-web/`

## F11 — Plataforma de acompanhamento (projeto interno)

108. **VTX-116** Verificador de status das conexões (somente leitura) → `vtx-acompanhamento/verificador/`

## F13 — Capacidades para o piloto plataforma-projetos

109. **VTX-145** Skill IFC no backend (IfcOpenShell 0.9, validação e IDS) → `.cursor/skills/ifc-python/`
110. **VTX-146** Padrão de biblioteca de funções de domínio para tool-calling da IA → `knowledge/engenharia/ia/funcoes-de-dominio.md`

## F11 — Plataforma de acompanhamento (projeto interno)

111. **VTX-090** Painel Markdown (semana 1): portfólio, fases e progresso → `vtx-acompanhamento/painel/`

## F13 — Capacidades para o piloto plataforma-projetos

112. **VTX-147** Execução isolada de código gerado por IA (sandbox) → `knowledge/seguranca/sandbox-codigo-ia.md`
113. **VTX-148** Orquestração de LLM: roteamento por modelo, streaming e fallback → `knowledge/engenharia/ia/orquestracao-llm.md`

## F11 — Plataforma de acompanhamento (projeto interno)

114. **VTX-117** Painel Markdown: conexões por projeto e alertas de conexão → `vtx-acompanhamento/painel/conexoes.md`

## F13 — Capacidades para o piloto plataforma-projetos

115. **VTX-149** Medição de tokens, franquia com pausa e chave própria (BYOK) → `knowledge/engenharia/ia/medicao-tokens-byok.md`
116. **VTX-150** Privacidade em IA: retenção zero, não treino e LGPD nos prompts → `knowledge/conformidade/ia-privacidade.md`

## F11 — Plataforma de acompanhamento (projeto interno)

117. **VTX-095** Plataforma: ADR da interface web com acesso restrito → `vtx-acompanhamento/docs/adr/`

## F13 — Capacidades para o piloto plataforma-projetos

118. **VTX-151** Versionamento de modelos IFC: versões, branches, diff e merge → `knowledge/engenharia/bim/versionamento-ifc.md`
119. **VTX-152** Prova de conceito: diff visual de IFC e desempenho 3D no navegador → `projects/plataforma-projetos/docs/poc/`

## F11 — Plataforma de acompanhamento (projeto interno)

120. **VTX-096** Interface web: estrutura, login restrito e portfólio → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

121. **VTX-153** Importação de arquivos: DWG/DXF só leitura e extração de PDF, DOCX e XLSX → `knowledge/engenharia/importacao-arquivos.md`
122. **VTX-154** Armazenamento de arquivos grandes com custo zero inicial → `knowledge/operacao/armazenamento-arquivos-grandes.md`

## F11 — Plataforma de acompanhamento (projeto interno)

123. **VTX-091** Interface web: atividade dos agentes e handoffs → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

124. **VTX-155** Assinaturas SaaS no Brasil: planos, créditos pré-pagos, Pix e webhooks → `knowledge/engenharia/assinaturas-saas-br.md`
125. **VTX-156** SaaS multi-inquilino: login Google, papéis por disciplina e convites → `knowledge/engenharia/saas-multitenant-auth.md`

## F11 — Plataforma de acompanhamento (projeto interno)

126. **VTX-092** Interface web: fila de aprovações e registro de decisões → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

127. **VTX-157** Comentários no modelo 3D (BCF) e notificações de andamento → `knowledge/engenharia/bim/comentarios-notificacoes.md`
128. **VTX-158** Páginas públicas de portfólio com SEO → `knowledge/engenharia/paginas-publicas-seo.md`

## F11 — Plataforma de acompanhamento (projeto interno)

129. **VTX-118** Interface web: ferramentas e conexões por projeto → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

130. **VTX-159** Quantitativos e memoriais gerados a partir do IFC → `.cursor/skills/ifc-quantitativos/`
131. **VTX-160** Termos de uso, política de privacidade e mapa de dados do piloto → `projects/plataforma-projetos/docs/juridico/`

## F11 — Plataforma de acompanhamento (projeto interno)

132. **VTX-093** Interface web: métricas, custos e alertas → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

133. **VTX-161** Programa alpha com 5 a 10 projetistas → `knowledge/processos/programa-alpha.md`
134. **VTX-162** Captura de dados para fine-tuning futuro (pedido → ação no IFC) → `knowledge/engenharia/ia/dataset-fine-tuning.md`

## F11 — Plataforma de acompanhamento (projeto interno)

135. **VTX-094** Plataforma: uso real por uma semana e decisão continuar ou pivotar → `vtx-acompanhamento/docs/relatorio-mvp.md`

## F13 — Capacidades para o piloto plataforma-projetos

136. **VTX-163** Avaliação de qualidade da IA (evals de modelagem IFC) → `knowledge/engenharia/ia/evals.md`
137. **VTX-164** Inventário das ferramentas Tekto para a v1 (Calc, Docs, Model) → `projects/plataforma-projetos/conhecimento/tekto-ferramentas.md`

## F11 — Plataforma de acompanhamento (projeto interno)

138. **VTX-097** Plataforma: incluir projetos de cliente e outros repositórios → `vtx-acompanhamento/gerador/`

## F13 — Capacidades para o piloto plataforma-projetos

139. **VTX-165** Métricas de produto SaaS (pagantes, churn, custo de IA por projeto) → `knowledge/operacao/metricas-produto-saas.md`

## F8 — Consolidação e validação

140. **VTX-047** Glossário técnico → `knowledge/glossario.md`
141. **VTX-048** Revisão geral da base (consistência, links, fontes) → `knowledge/`
142. **VTX-049** Índice final e guia de navegação para agentes → `knowledge/INDEX.md`
143. **VTX-050** Projeto piloto: definição, triagem do tipo e PRD → `projects/plataforma-projetos/`
144. **VTX-051** Projeto piloto: execução do fluxo completo → `projects/plataforma-projetos/`
145. **VTX-052** Projeto piloto: retrospectiva e ajustes na base → `projects/plataforma-projetos/`
146. **VTX-073** Validação automática do backlog no CI (ids, campos, status, dependências) → `scripts/validar_backlog.py`
147. **VTX-074** Verificação automática de links e fontes da base de conhecimento → `.github/workflows/links.yml`
148. **VTX-075** ROADMAP gerado com status efetivo (só tarefas pendentes) → `scripts/gerar_roadmap.py`

## F10 — Arsenal de scripts e papéis administrativos

149. **VTX-076** Inventário de tarefas recorrentes de desenvolvimento para o arsenal de scripts → `scripts/arsenal/INVENTARIO.md`
150. **VTX-077** Script de estrutura inicial de projeto por tipo → `scripts/arsenal/scaffold.py`
151. **VTX-078** Script de checklist automatizado de revisão de código e qualidade → `scripts/arsenal/revisao.py`
152. **VTX-079** Script de verificações de segurança (dependências e segredos) → `scripts/arsenal/seguranca.py`
153. **VTX-080** Script de verificação de prontidão para deploy → `scripts/arsenal/prontidao_deploy.py`
154. **VTX-081** Skills: receitas curtas que usam o arsenal de scripts → `skills/`
155. **VTX-082** Adotar o formato-fonte de agentes e os exportadores compartilhados → `agentes/`
156. **VTX-083** Papéis administrativos para software house (comercial, financeiro, jurídico e LGPD) → `knowledge/papeis/administrativos/`
