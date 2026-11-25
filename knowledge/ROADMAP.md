# Roadmap da Base de Conhecimento

Gerado por `scripts/gerar_roadmap.py` a partir do status efetivo do backlog (mestre + diários).
Só entram tarefas ainda não concluídas nem canceladas, em ordem de prioridade. Próxima: `python scripts/proxima_tarefa.py`.
Ao concluir um documento, adicioná-lo ao `INDEX.md`.

## F8 — Consolidação e validação

1. **VTX-167** Status aguardando e cancelado no backlog, e VTX-142 cancelada (auditoria P0) → `scripts/backlog_lib.py + backlog/SCHEMA.md + scripts/proxima_tarefa.py`
2. **VTX-168** Portão de qualidade no CI (auditoria P0 item 4) → `.github/workflows/testes.yml + scripts/validar_backlog.py + scripts/verificar_links.py`

## F9 — Integração com o Cursor e operação

3. **VTX-169** AGENTS.md e regras por papel (auditoria P0 item 2) → `AGENTS.md + .cursor/rules/papeis/planejamento.mdc + .cursor/rules/papeis/execucao.mdc`

## F6 — Templates de artefatos

4. **VTX-170** Template de projeto de cliente e script de bootstrap (auditoria P0 item 3) → `templates/projeto/ + scripts/bootstrap_projeto.sh`

## F11 — Plataforma de acompanhamento (projeto interno)

5. **VTX-171** Corrigir ou aposentar o pipeline do painel (auditoria P0 item 1) → `README.md + backlog/SCHEMA.md + .github/workflows/sincronizar-painel.yml`

## F1 — Processo e operação de agentes

6. **VTX-172** Revisão obrigatória antes do merge (auditoria P0 item 6) → `.github/pull_request_template.md + .github/CODEOWNERS + knowledge/processos/governanca-e-aprovacoes.md`

## F12 — Catálogo de ferramentas

7. **VTX-135** Piloto local do Trail-code (graft map) como ferramenta do mapa de codebase → `knowledge/ferramentas/piloto-trail-code.md`
8. **VTX-136** Observação contínua de skills e revisão na manutenção quinzenal (adaptado do task-observer) → `knowledge/processos/observacao-de-skills.md`
9. **VTX-137** Processo de melhoria do harness da VTX no Cursor (metodologia do Harness²) → `knowledge/processos/melhoria-do-harness.md`
10. **VTX-140** Skills do ECC que preenchem lacunas do stack VTX → `.cursor/skills/ (verification-loop, tdd-workflow, search-first, context-budget, security-review, e2e-testing, api-design, postgres-patterns, deployment-patterns, mcp-dependency-review)`

## F5 — Gestão e conformidade

11. **VTX-029** Gestão de projetos, riscos e comunicação com cliente → `knowledge/gestao/gestao-de-projetos.md`
12. **VTX-030** Estimativas e planejamento → `knowledge/gestao/estimativas.md`
13. **VTX-031** LGPD e compliance → `knowledge/seguranca/lgpd-compliance.md`
14. **VTX-032** Documentação técnica (docs-as-code) → `knowledge/gestao/documentacao-tecnica.md`

## F6 — Templates de artefatos

15. **VTX-033** Template de PRD → `knowledge/templates/prd.md`
16. **VTX-034** Template de história de usuário e critérios de aceite → `knowledge/templates/historia-de-usuario.md`
17. **VTX-035** Template de ADR → `knowledge/templates/adr.md`
18. **VTX-036** Template de plano e relatório de testes → `knowledge/templates/plano-de-testes.md`
19. **VTX-037** Template de runbook e postmortem → `knowledge/templates/runbook-postmortem.md`
20. **VTX-038** Template de relatório diário e de sprint → `knowledge/templates/relatorios.md`

## F7 — Diretrizes por papel

21. **VTX-039** Diretrizes do agente Orquestrador → `knowledge/diretrizes/orquestrador.md`
22. **VTX-040** Diretrizes do agente Produto → `knowledge/diretrizes/produto.md`
23. **VTX-041** Diretrizes do agente Arquiteto → `knowledge/diretrizes/arquiteto.md`
24. **VTX-042** Diretrizes do agente Dev Backend → `knowledge/diretrizes/dev-backend.md`
25. **VTX-043** Diretrizes do agente Dev Frontend/Mobile → `knowledge/diretrizes/dev-frontend-mobile.md`
26. **VTX-044** Diretrizes do agente QA → `knowledge/diretrizes/qa.md`
27. **VTX-045** Diretrizes do agente DevOps/SRE → `knowledge/diretrizes/devops-sre.md`
28. **VTX-046** Diretrizes dos especialistas sob demanda → `knowledge/diretrizes/especialistas.md`

## F9 — Integração com o Cursor e operação

29. **VTX-053** AGENTS.md raiz com diretrizes gerais dos agentes → `AGENTS.md`
30. **VTX-054** Regra sempre ativa: fluxo entre papéis, DoD e aprovações → `.cursor/rules/vtx-base.mdc`
31. **VTX-055** Regras por papel: Orquestrador, Produto e Arquiteto → `.cursor/rules/papeis/planejamento.mdc`
32. **VTX-056** Regras por papel: Devs, QA e DevOps/SRE → `.cursor/rules/papeis/execucao.mdc`
33. **VTX-134** Enriquecer papéis de agentes com o catálogo agency-agents → `knowledge/organizacao/papeis-de-agentes.md`
34. **VTX-057** Regras por assunto com globs: testes e APIs → `.cursor/rules/assuntos/testes-api.mdc`
35. **VTX-058** Regras por assunto com globs: frontend/mobile e segurança → `.cursor/rules/assuntos/frontend-seguranca.mdc`
36. **VTX-138** Regras comuns e por stack em .cursor/rules a partir do ECC → `.cursor/rules/ (common-*, typescript, react, react-native, python) e knowledge/templates/cursor/`
37. **VTX-139** Hooks do Cursor como guardrails locais (adaptados do ECC) → `.cursor/hooks.json e scripts/hooks/ (padrão TT-060)`
38. **VTX-059** Estratégia de consulta sob demanda e índice para agentes → `knowledge/index.yaml`
39. **VTX-060** Template de repositório de projeto → `templates/projeto/`
40. **VTX-061** Sincronização de regras e script de bootstrap de projetos → `scripts/bootstrap_projeto.sh`
41. **VTX-062** Ambiente dos agentes de nuvem (environment.json, segredos, permissões) → `.cursor/environment.json`
42. **VTX-063** Orquestração com issues, PRs e agentes de nuvem por papel e tipo de projeto → `knowledge/processos/orquestracao-cursor.md`
43. **VTX-064** Pontos de aprovação do Samuel (branch protegida, revisões, release) → `knowledge/processos/pontos-de-aprovacao.md`
44. **VTX-065** Teste de validação da integração com o Cursor → `projects/validacao-cursor/`

## F11 — Plataforma de acompanhamento (projeto interno)

45. **VTX-086** Plataforma: PRD do MVP, hipóteses e critérios de sucesso → `vtx-acompanhamento/docs/prd-mvp.md`
46. **VTX-087** Formatos de registro: eventos, handoffs, decisões e custos → `registro/ + backlog/SCHEMA.md`
47. **VTX-088** Formato da fila de aprovações do Samuel → `registro/aprovacoes.yaml + backlog/SCHEMA.md`
48. **VTX-115** Esquema do manifesto de conexões por projeto → `projects/CONEXOES.md + projects/<p>/conexoes.yaml`
49. **VTX-089** Gerador de dados da plataforma (JSON privado único) → `vtx-acompanhamento/gerador/`
50. **VTX-116** Verificador de status das conexões (somente leitura) → `vtx-acompanhamento/verificador/`
51. **VTX-090** Painel Markdown (semana 1): portfólio, fases e progresso → `vtx-acompanhamento/painel/`

## F13 — Capacidades para o piloto plataforma-projetos

52. **VTX-147** Execução isolada de código gerado por IA (sandbox) → `knowledge/seguranca/sandbox-codigo-ia.md`
53. **VTX-148** Orquestração de LLM: roteamento por modelo, streaming e fallback → `knowledge/engenharia/ia/orquestracao-llm.md`

## F11 — Plataforma de acompanhamento (projeto interno)

54. **VTX-117** Painel Markdown: conexões por projeto e alertas de conexão → `vtx-acompanhamento/painel/conexoes.md`

## F13 — Capacidades para o piloto plataforma-projetos

55. **VTX-149** Medição de tokens, franquia com pausa e chave própria (BYOK) → `knowledge/engenharia/ia/medicao-tokens-byok.md`
56. **VTX-150** Privacidade em IA: retenção zero, não treino e LGPD nos prompts → `knowledge/conformidade/ia-privacidade.md`

## F11 — Plataforma de acompanhamento (projeto interno)

57. **VTX-095** Plataforma: ADR da interface web com acesso restrito → `vtx-acompanhamento/docs/adr/`

## F13 — Capacidades para o piloto plataforma-projetos

58. **VTX-152** Prova de conceito: banco de objetos como camada de trabalho, diff visual e desempenho 3D → `projects/plataforma-projetos/docs/poc/`

## F11 — Plataforma de acompanhamento (projeto interno)

59. **VTX-096** Interface web: estrutura, login restrito e portfólio → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

60. **VTX-153** Importação de arquivos: DWG/DXF só leitura e extração de PDF, DOCX e XLSX → `knowledge/engenharia/importacao-arquivos.md`
61. **VTX-154** Armazenamento de arquivos grandes com custo zero inicial → `knowledge/operacao/armazenamento-arquivos-grandes.md`

## F11 — Plataforma de acompanhamento (projeto interno)

62. **VTX-091** Interface web: atividade dos agentes e handoffs → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

63. **VTX-155** Assinaturas SaaS no Brasil: planos, créditos pré-pagos, Pix e webhooks → `knowledge/engenharia/assinaturas-saas-br.md`
64. **VTX-156** SaaS multi-inquilino: login Google, papéis por disciplina e convites → `knowledge/engenharia/saas-multitenant-auth.md`

## F11 — Plataforma de acompanhamento (projeto interno)

65. **VTX-092** Interface web: fila de aprovações e registro de decisões → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

66. **VTX-157** Comentários no modelo 3D (BCF) e notificações de andamento → `knowledge/engenharia/bim/comentarios-notificacoes.md`
67. **VTX-158** Páginas públicas de portfólio com SEO → `knowledge/engenharia/paginas-publicas-seo.md`

## F11 — Plataforma de acompanhamento (projeto interno)

68. **VTX-118** Interface web: ferramentas e conexões por projeto → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

69. **VTX-159** Quantitativos e memoriais gerados a partir do IFC → `.cursor/skills/ifc-quantitativos/`
70. **VTX-160** Termos de uso, política de privacidade e mapa de dados do piloto → `projects/plataforma-projetos/docs/juridico/`

## F11 — Plataforma de acompanhamento (projeto interno)

71. **VTX-093** Interface web: métricas, custos e alertas → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

72. **VTX-161** Programa alpha com 5 a 10 projetistas → `knowledge/processos/programa-alpha.md`
73. **VTX-162** Captura de dados para fine-tuning futuro (pedido → ação no IFC) → `knowledge/engenharia/ia/dataset-fine-tuning.md`

## F11 — Plataforma de acompanhamento (projeto interno)

74. **VTX-094** Plataforma: uso real por uma semana e decisão continuar ou pivotar → `vtx-acompanhamento/docs/relatorio-mvp.md`

## F13 — Capacidades para o piloto plataforma-projetos

75. **VTX-163** Avaliação de qualidade da IA (evals de modelagem IFC) → `knowledge/engenharia/ia/evals.md`
76. **VTX-164** Inventário das ferramentas Tekto para a v1 (Calc, Docs, Model) → `projects/plataforma-projetos/conhecimento/tekto-ferramentas.md`

## F11 — Plataforma de acompanhamento (projeto interno)

77. **VTX-097** Plataforma: incluir projetos de cliente e outros repositórios → `vtx-acompanhamento/gerador/`

## F13 — Capacidades para o piloto plataforma-projetos

78. **VTX-165** Métricas de produto SaaS (pagantes, churn, custo de IA por projeto) → `knowledge/operacao/metricas-produto-saas.md`

## F8 — Consolidação e validação

79. **VTX-047** Glossário técnico → `knowledge/glossario.md`
80. **VTX-048** Revisão geral da base (consistência, links, fontes) → `knowledge/`
81. **VTX-049** Índice final e guia de navegação para agentes → `knowledge/INDEX.md`
82. **VTX-050** Projeto piloto: definição, triagem do tipo e PRD → `projects/plataforma-projetos/`
83. **VTX-051** Projeto piloto: execução do fluxo completo → `projects/plataforma-projetos/`
84. **VTX-052** Projeto piloto: retrospectiva e ajustes na base → `projects/plataforma-projetos/`
85. **VTX-073** Validação automática do backlog no CI (ids, campos, status, dependências) → `scripts/validar_backlog.py`
86. **VTX-074** Verificação automática de links e fontes da base de conhecimento → `.github/workflows/links.yml`
87. **VTX-075** ROADMAP gerado com status efetivo (só tarefas pendentes) → `scripts/gerar_roadmap.py`

## F10 — Arsenal de scripts e papéis administrativos

88. **VTX-076** Inventário de tarefas recorrentes de desenvolvimento para o arsenal de scripts → `scripts/arsenal/INVENTARIO.md`
89. **VTX-077** Script de estrutura inicial de projeto por tipo → `scripts/arsenal/scaffold.py`
90. **VTX-078** Script de checklist automatizado de revisão de código e qualidade → `scripts/arsenal/revisao.py`
91. **VTX-079** Script de verificações de segurança (dependências e segredos) → `scripts/arsenal/seguranca.py`
92. **VTX-080** Script de verificação de prontidão para deploy → `scripts/arsenal/prontidao_deploy.py`
93. **VTX-081** Skills: receitas curtas que usam o arsenal de scripts → `skills/`
94. **VTX-082** Adotar o formato-fonte de agentes e os exportadores compartilhados → `agentes/`
95. **VTX-083** Papéis administrativos para software house (comercial, financeiro, jurídico e LGPD) → `knowledge/papeis/administrativos/`
