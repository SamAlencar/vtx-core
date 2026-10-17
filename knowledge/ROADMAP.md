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
9. **VTX-072** Fluxo de projeto: MVP / prova de conceito → `knowledge/processos/fluxos/mvp-poc.md`
10. **VTX-011** Engenharia de requisitos → `knowledge/processos/engenharia-de-requisitos.md`
11. **VTX-012** Scrum e Kanban adaptados a agentes → `knowledge/processos/scrum-kanban-agentes.md`
12. **VTX-013** Operação de agentes: prompts, contexto e memória → `knowledge/processos/operacao-de-agentes.md`
13. **VTX-014** Governança e aprovações (humano no circuito) → `knowledge/processos/governanca-e-aprovacoes.md`

## F2 — Engenharia de software

14. **VTX-015** Arquitetura de software (estilos, C4, ADRs) → `knowledge/engenharia/arquitetura-de-software.md`
15. **VTX-016** Padrões de projeto e DDD → `knowledge/engenharia/padroes-de-projeto-ddd.md`
16. **VTX-017** Padrões de código, Clean Code e code review → `knowledge/engenharia/padroes-de-codigo.md`
17. **VTX-018** Estratégia de testes e qualidade → `knowledge/engenharia/testes-e-qualidade.md`
18. **VTX-019** Git e CI/CD → `knowledge/engenharia/git-e-ci-cd.md`

## F3 — Segurança e operação

19. **VTX-020** Segurança no desenvolvimento (OWASP, SSDF) → `knowledge/seguranca/desenvolvimento-seguro.md`
20. **VTX-021** DevOps e SRE (IaC, SLOs, incidentes) → `knowledge/operacao/devops-sre.md`
21. **VTX-022** Observabilidade (logs, métricas, traces) → `knowledge/operacao/observabilidade.md`

## F4 — Tecnologia e plataformas

22. **VTX-023** Stack de referência da VTX → `knowledge/tecnologia/stack-de-referencia.md`
23. **VTX-024** Design de APIs → `knowledge/tecnologia/design-de-apis.md`
24. **VTX-025** Modelagem de dados e bancos de dados → `knowledge/tecnologia/modelagem-de-dados.md`
25. **VTX-026** Desenvolvimento frontend web → `knowledge/tecnologia/frontend-web.md`
26. **VTX-027** Desenvolvimento mobile → `knowledge/tecnologia/mobile.md`
27. **VTX-028** UX/UI e acessibilidade → `knowledge/tecnologia/ux-ui-acessibilidade.md`

## F12 — Catálogo de ferramentas

28. **VTX-098** Base do catálogo de ferramentas (estrutura, modelo, critérios, matriz) → `knowledge/ferramentas/README.md`
29. **VTX-099** Ferramenta: Vercel → `knowledge/ferramentas/hospedagem/vercel.md`
30. **VTX-100** Ferramenta: Supabase (banco, auth, storage) → `knowledge/ferramentas/backend/supabase.md`
31. **VTX-101** Ferramenta: GitHub e GitHub Actions → `knowledge/ferramentas/ci-cd/github-actions.md`
32. **VTX-102** Ferramenta: Cursor (regras, agentes locais e na nuvem) → `knowledge/ferramentas/ia-dev/cursor.md`
33. **VTX-103** Ferramenta: Appwrite → `knowledge/ferramentas/backend/appwrite.md`
34. **VTX-104** Ferramenta: Firebase → `knowledge/ferramentas/backend/firebase.md`
35. **VTX-105** Ferramenta: Expo e EAS → `knowledge/ferramentas/mobile/expo.md`
36. **VTX-106** Ferramentas de pagamento: Stripe e Mercado Pago → `knowledge/ferramentas/pagamentos/stripe-mercado-pago.md`
37. **VTX-107** Ferramenta: Sentry → `knowledge/ferramentas/observabilidade/sentry.md`
38. **VTX-108** Ferramenta: Cloudflare (DNS, Pages, Access, WAF) → `knowledge/ferramentas/ci-cd/cloudflare.md`
39. **VTX-109** Ferramenta: Docker → `knowledge/ferramentas/ci-cd/docker.md`
40. **VTX-110** Ferramenta: Figma → `knowledge/ferramentas/design/figma.md`
41. **VTX-111** Ferramentas de comunicação e gestão (Google Workspace, Grok Bot) → `knowledge/ferramentas/comunicacao/google-workspace.md`
42. **VTX-112** Matriz ferramenta × fluxo completa e links nos fluxos → `knowledge/ferramentas/README.md`
43. **VTX-113** Processo periódico de revisão de ferramentas → `knowledge/ferramentas/revisao-periodica.md`
44. **VTX-119** Bibliotecas e recursos para agentes: processo e registro → `knowledge/ferramentas/bibliotecas-e-recursos.md`
45. **VTX-120** Pesquisa de recursos: frontend, UI e design → `knowledge/ferramentas/recursos.yaml`
46. **VTX-121** Pesquisa de recursos: backend e APIs → `knowledge/ferramentas/recursos.yaml`
47. **VTX-122** Pesquisa de recursos: testes e QA → `knowledge/ferramentas/recursos.yaml`
48. **VTX-123** Pesquisa de recursos: segurança e cadeia de suprimentos → `knowledge/ferramentas/recursos.yaml`
49. **VTX-124** Pesquisa de recursos: documentação → `knowledge/ferramentas/recursos.yaml`
50. **VTX-125** Pesquisa de recursos: skills de agentes e regras do Cursor → `knowledge/ferramentas/recursos.yaml`
51. **VTX-126** Pesquisa de recursos: servidores MCP → `knowledge/ferramentas/recursos.yaml`
52. **VTX-127** Piloto do impeccable em uma tela de teste (fluxo frontend) → `projects/sandbox-impeccable/`
53. **VTX-128** Integrar o registro de recursos às definições dos agentes e aos fluxos → `agents/ + knowledge/processos/fluxos/`
54. **VTX-129** Varredura periódica de recursos na manutenção quinzenal e revisão trimestral → `knowledge/ferramentas/revisao-periodica.md`

## F5 — Gestão e conformidade

55. **VTX-029** Gestão de projetos, riscos e comunicação com cliente → `knowledge/gestao/gestao-de-projetos.md`
56. **VTX-030** Estimativas e planejamento → `knowledge/gestao/estimativas.md`
57. **VTX-031** LGPD e compliance → `knowledge/seguranca/lgpd-compliance.md`
58. **VTX-032** Documentação técnica (docs-as-code) → `knowledge/gestao/documentacao-tecnica.md`

## F6 — Templates de artefatos

59. **VTX-033** Template de PRD → `knowledge/templates/prd.md`
60. **VTX-034** Template de história de usuário e critérios de aceite → `knowledge/templates/historia-de-usuario.md`
61. **VTX-035** Template de ADR → `knowledge/templates/adr.md`
62. **VTX-036** Template de plano e relatório de testes → `knowledge/templates/plano-de-testes.md`
63. **VTX-037** Template de runbook e postmortem → `knowledge/templates/runbook-postmortem.md`
64. **VTX-038** Template de relatório diário e de sprint → `knowledge/templates/relatorios.md`

## F7 — Diretrizes por papel

65. **VTX-039** Diretrizes do agente Orquestrador → `knowledge/diretrizes/orquestrador.md`
66. **VTX-040** Diretrizes do agente Produto → `knowledge/diretrizes/produto.md`
67. **VTX-041** Diretrizes do agente Arquiteto → `knowledge/diretrizes/arquiteto.md`
68. **VTX-042** Diretrizes do agente Dev Backend → `knowledge/diretrizes/dev-backend.md`
69. **VTX-043** Diretrizes do agente Dev Frontend/Mobile → `knowledge/diretrizes/dev-frontend-mobile.md`
70. **VTX-044** Diretrizes do agente QA → `knowledge/diretrizes/qa.md`
71. **VTX-045** Diretrizes do agente DevOps/SRE → `knowledge/diretrizes/devops-sre.md`
72. **VTX-046** Diretrizes dos especialistas sob demanda → `knowledge/diretrizes/especialistas.md`

## F9 — Integração com o Cursor e operação

73. **VTX-053** AGENTS.md raiz com diretrizes gerais dos agentes → `AGENTS.md`
74. **VTX-054** Regra sempre ativa: fluxo entre papéis, DoD e aprovações → `.cursor/rules/vtx-base.mdc`
75. **VTX-055** Regras por papel: Orquestrador, Produto e Arquiteto → `.cursor/rules/papeis/planejamento.mdc`
76. **VTX-056** Regras por papel: Devs, QA e DevOps/SRE → `.cursor/rules/papeis/execucao.mdc`
77. **VTX-057** Regras por assunto com globs: testes e APIs → `.cursor/rules/assuntos/testes-api.mdc`
78. **VTX-058** Regras por assunto com globs: frontend/mobile e segurança → `.cursor/rules/assuntos/frontend-seguranca.mdc`
79. **VTX-059** Estratégia de consulta sob demanda e índice para agentes → `knowledge/index.yaml`
80. **VTX-060** Template de repositório de projeto → `templates/projeto/`
81. **VTX-061** Sincronização de regras e script de bootstrap de projetos → `scripts/bootstrap_projeto.sh`
82. **VTX-062** Ambiente dos agentes de nuvem (environment.json, segredos, permissões) → `.cursor/environment.json`
83. **VTX-063** Orquestração com issues, PRs e agentes de nuvem por papel e tipo de projeto → `knowledge/processos/orquestracao-cursor.md`
84. **VTX-064** Pontos de aprovação do Samuel (branch protegida, revisões, release) → `knowledge/processos/pontos-de-aprovacao.md`
85. **VTX-065** Teste de validação da integração com o Cursor → `projects/validacao-cursor/`

## F11 — Plataforma de acompanhamento (projeto interno)

86. **VTX-085** Planejamento da plataforma de acompanhamento → `knowledge/projetos-internos/plataforma-acompanhamento.md`
87. **VTX-114** Plataforma: revisão do plano (ferramentas, conexões, Cursor primeiro) → `knowledge/projetos-internos/plataforma-acompanhamento.md`
88. **VTX-086** Plataforma: PRD do MVP, hipóteses e critérios de sucesso → `vtx-acompanhamento/docs/prd-mvp.md`
89. **VTX-087** Formatos de registro: eventos, handoffs, decisões e custos → `registro/ + backlog/SCHEMA.md`
90. **VTX-088** Formato da fila de aprovações do Samuel → `registro/aprovacoes.yaml + backlog/SCHEMA.md`
91. **VTX-115** Esquema do manifesto de conexões por projeto → `projects/CONEXOES.md + projects/<p>/conexoes.yaml`
92. **VTX-089** Gerador de dados da plataforma (JSON privado único) → `vtx-acompanhamento/gerador/`
93. **VTX-116** Verificador de status das conexões (somente leitura) → `vtx-acompanhamento/verificador/`
94. **VTX-090** Painel Markdown (semana 1): portfólio, fases e progresso → `vtx-acompanhamento/painel/`
95. **VTX-117** Painel Markdown: conexões por projeto e alertas de conexão → `vtx-acompanhamento/painel/conexoes.md`
96. **VTX-095** Plataforma: ADR da interface web com acesso restrito → `vtx-acompanhamento/docs/adr/`
97. **VTX-096** Interface web: estrutura, login restrito e portfólio → `vtx-acompanhamento/web/`
98. **VTX-091** Interface web: atividade dos agentes e handoffs → `vtx-acompanhamento/web/`
99. **VTX-092** Interface web: fila de aprovações e registro de decisões → `vtx-acompanhamento/web/`
100. **VTX-118** Interface web: ferramentas e conexões por projeto → `vtx-acompanhamento/web/`
101. **VTX-093** Interface web: métricas, custos e alertas → `vtx-acompanhamento/web/`
102. **VTX-094** Plataforma: uso real por uma semana e decisão continuar ou pivotar → `vtx-acompanhamento/docs/relatorio-mvp.md`
103. **VTX-097** Plataforma: incluir projetos de cliente e outros repositórios → `vtx-acompanhamento/gerador/`

## F8 — Consolidação e validação

104. **VTX-047** Glossário técnico → `knowledge/glossario.md`
105. **VTX-048** Revisão geral da base (consistência, links, fontes) → `knowledge/`
106. **VTX-049** Índice final e guia de navegação para agentes → `knowledge/INDEX.md`
107. **VTX-050** Projeto piloto: definição, triagem do tipo e PRD → `projects/piloto/`
108. **VTX-051** Projeto piloto: execução do fluxo completo → `projects/piloto/`
109. **VTX-052** Projeto piloto: retrospectiva e ajustes na base → `projects/piloto/`
110. **VTX-073** Validação automática do backlog no CI (ids, campos, status, dependências) → `scripts/validar_backlog.py`
111. **VTX-074** Verificação automática de links e fontes da base de conhecimento → `.github/workflows/links.yml`
112. **VTX-075** ROADMAP gerado com status efetivo (só tarefas pendentes) → `scripts/gerar_roadmap.py`

## F10 — Arsenal de scripts e papéis administrativos

113. **VTX-076** Inventário de tarefas recorrentes de desenvolvimento para o arsenal de scripts → `scripts/arsenal/INVENTARIO.md`
114. **VTX-077** Script de estrutura inicial de projeto por tipo → `scripts/arsenal/scaffold.py`
115. **VTX-078** Script de checklist automatizado de revisão de código e qualidade → `scripts/arsenal/revisao.py`
116. **VTX-079** Script de verificações de segurança (dependências e segredos) → `scripts/arsenal/seguranca.py`
117. **VTX-080** Script de verificação de prontidão para deploy → `scripts/arsenal/prontidao_deploy.py`
118. **VTX-081** Skills: receitas curtas que usam o arsenal de scripts → `skills/`
119. **VTX-082** Adotar o formato-fonte de agentes e os exportadores compartilhados → `agentes/`
120. **VTX-083** Papéis administrativos para software house (comercial, financeiro, jurídico e LGPD) → `knowledge/papeis/administrativos/`
