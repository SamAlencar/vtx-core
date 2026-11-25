# Roadmap da Base de Conhecimento

Gerado por `scripts/gerar_roadmap.py` a partir do status efetivo do backlog (mestre + diários).
Só entram tarefas ainda não concluídas nem canceladas, em ordem de prioridade. Próxima: `python scripts/proxima_tarefa.py`.
Ao concluir um documento, adicioná-lo ao `INDEX.md`.

## F1 — Processo e operação de agentes

1. **VTX-172** Revisão obrigatória antes do merge (auditoria P0 item 6) → `.github/pull_request_template.md + .github/CODEOWNERS + knowledge/processos/governanca-e-aprovacoes.md`

## F3 — Segurança e operação

2. **VTX-173** Higiene de segredos (.gitignore, .env.example e pre-commit com gitleaks) → `.gitignore + .env.example + .pre-commit-config.yaml`

## F9 — Integração com o Cursor e operação

3. **VTX-180** Remover a duplicação da regra de eficiência de tokens → `.cursor/rules/eficiencia-de-tokens.mdc + knowledge/templates/cursor/eficiencia-de-tokens.mdc`

## F1 — Processo e operação de agentes

4. **VTX-174** Human-in-the-loop verificável (evidência de aprovação A2) → `backlog/SCHEMA.md + scripts/validar_backlog.py`

## F13 — Capacidades para o piloto plataforma-projetos

5. **VTX-176** Empacotar o núcleo de funções de domínio (core/vtx_ifc) → `pyproject.toml + core/vtx_ifc/`
6. **VTX-177** Harness de agente de referência (loop de tool-calling) → `core/agente/loop.py + tests/test_loop_agente.py + knowledge/engenharia/ia/orquestracao-llm.md`

## F12 — Catálogo de ferramentas

7. **VTX-135** Piloto local do Trail-code (graft map) como ferramenta do mapa de codebase → `knowledge/ferramentas/piloto-trail-code.md`
8. **VTX-136** Observação contínua de skills e revisão na manutenção quinzenal (adaptado do task-observer) → `knowledge/processos/observacao-de-skills.md`
9. **VTX-137** Processo de melhoria do harness da VTX no Cursor (metodologia do Harness²) → `knowledge/processos/melhoria-do-harness.md`
10. **VTX-140** Skills do ECC que preenchem lacunas do stack VTX → `.cursor/skills/ (verification-loop, tdd-workflow, search-first, context-budget, security-review, e2e-testing, api-design, postgres-patterns, deployment-patterns, mcp-dependency-review)`

## F5 — Gestão e conformidade

11. **VTX-029** Gestão de projetos, riscos e comunicação com cliente → `knowledge/gestao/gestao-de-projetos.md`
12. **VTX-030** Estimativas e planejamento → `knowledge/gestao/estimativas.md`

## F13 — Capacidades para o piloto plataforma-projetos

13. **VTX-178** Suíte de evals mínima com portão no CI → `evals/README.md + evals/executar.py + knowledge/engenharia/ia/evals.md`

## F5 — Gestão e conformidade

14. **VTX-031** LGPD e compliance → `knowledge/seguranca/lgpd-compliance.md`

## F13 — Capacidades para o piloto plataforma-projetos

15. **VTX-179** Log estruturado por execução de agente e custo → `core/agente/telemetria.py + knowledge/operacao/observabilidade.md`

## F5 — Gestão e conformidade

16. **VTX-032** Documentação técnica (docs-as-code) → `knowledge/gestao/documentacao-tecnica.md`

## F8 — Consolidação e validação

17. **VTX-181** Lint de código e de Markdown no CI (ruff e markdownlint) → `pyproject.toml + .markdownlint.json + .github/workflows/testes.yml`

## F6 — Templates de artefatos

18. **VTX-033** Template de PRD → `knowledge/templates/prd.md`
19. **VTX-034** Template de história de usuário e critérios de aceite → `knowledge/templates/historia-de-usuario.md`
20. **VTX-035** Template de ADR → `knowledge/templates/adr.md`
21. **VTX-036** Template de plano e relatório de testes → `knowledge/templates/plano-de-testes.md`

## F8 — Consolidação e validação

22. **VTX-183** Exemplo ponta a ponta de agente rodando (onboarding) → `projects/exemplo-agente/`

## F6 — Templates de artefatos

23. **VTX-037** Template de runbook e postmortem → `knowledge/templates/runbook-postmortem.md`
24. **VTX-038** Template de relatório diário e de sprint → `knowledge/templates/relatorios.md`

## F7 — Diretrizes por papel

25. **VTX-039** Diretrizes do agente Orquestrador → `knowledge/diretrizes/orquestrador.md`
26. **VTX-040** Diretrizes do agente Produto → `knowledge/diretrizes/produto.md`
27. **VTX-041** Diretrizes do agente Arquiteto → `knowledge/diretrizes/arquiteto.md`
28. **VTX-042** Diretrizes do agente Dev Backend → `knowledge/diretrizes/dev-backend.md`
29. **VTX-043** Diretrizes do agente Dev Frontend/Mobile → `knowledge/diretrizes/dev-frontend-mobile.md`
30. **VTX-044** Diretrizes do agente QA → `knowledge/diretrizes/qa.md`
31. **VTX-045** Diretrizes do agente DevOps/SRE → `knowledge/diretrizes/devops-sre.md`
32. **VTX-046** Diretrizes dos especialistas sob demanda → `knowledge/diretrizes/especialistas.md`

## F9 — Integração com o Cursor e operação

33. **VTX-053** AGENTS.md raiz com diretrizes gerais dos agentes → `AGENTS.md`
34. **VTX-054** Regra sempre ativa: fluxo entre papéis, DoD e aprovações → `.cursor/rules/vtx-base.mdc`
35. **VTX-055** Regras por papel: Orquestrador, Produto e Arquiteto → `.cursor/rules/papeis/planejamento.mdc`
36. **VTX-056** Regras por papel: Devs, QA e DevOps/SRE → `.cursor/rules/papeis/execucao.mdc`
37. **VTX-134** Enriquecer papéis de agentes com o catálogo agency-agents → `knowledge/organizacao/papeis-de-agentes.md`
38. **VTX-057** Regras por assunto com globs: testes e APIs → `.cursor/rules/assuntos/testes-api.mdc`
39. **VTX-058** Regras por assunto com globs: frontend/mobile e segurança → `.cursor/rules/assuntos/frontend-seguranca.mdc`
40. **VTX-138** Regras comuns e por stack em .cursor/rules a partir do ECC → `.cursor/rules/ (common-*, typescript, react, react-native, python) e knowledge/templates/cursor/`
41. **VTX-139** Hooks do Cursor como guardrails locais (adaptados do ECC) → `.cursor/hooks.json e scripts/hooks/ (padrão TT-060)`
42. **VTX-059** Estratégia de consulta sob demanda e índice para agentes → `knowledge/index.yaml`

## F7 — Diretrizes por papel

43. **VTX-182** Diretrizes por papel (F7) e sincronização da tabela Recursos por papel → `knowledge/diretrizes/ + scripts/gerar_recursos_por_papel.py`

## F9 — Integração com o Cursor e operação

44. **VTX-060** Template de repositório de projeto → `templates/projeto/`
45. **VTX-061** Sincronização de regras e script de bootstrap de projetos → `scripts/bootstrap_projeto.sh`
46. **VTX-062** Ambiente dos agentes de nuvem (environment.json, segredos, permissões) → `.cursor/environment.json`
47. **VTX-063** Orquestração com issues, PRs e agentes de nuvem por papel e tipo de projeto → `knowledge/processos/orquestracao-cursor.md`
48. **VTX-064** Pontos de aprovação do Samuel (branch protegida, revisões, release) → `knowledge/processos/pontos-de-aprovacao.md`
49. **VTX-065** Teste de validação da integração com o Cursor → `projects/validacao-cursor/`

## F11 — Plataforma de acompanhamento (projeto interno)

50. **VTX-086** Plataforma: PRD do MVP, hipóteses e critérios de sucesso → `vtx-acompanhamento/docs/prd-mvp.md`
51. **VTX-087** Formatos de registro: eventos, handoffs, decisões e custos → `registro/ + backlog/SCHEMA.md`
52. **VTX-088** Formato da fila de aprovações do Samuel → `registro/aprovacoes.yaml + backlog/SCHEMA.md`
53. **VTX-115** Esquema do manifesto de conexões por projeto → `projects/CONEXOES.md + projects/<p>/conexoes.yaml`
54. **VTX-089** Gerador de dados da plataforma (JSON privado único) → `vtx-acompanhamento/gerador/`
55. **VTX-116** Verificador de status das conexões (somente leitura) → `vtx-acompanhamento/verificador/`
56. **VTX-090** Painel Markdown (semana 1): portfólio, fases e progresso → `vtx-acompanhamento/painel/`

## F13 — Capacidades para o piloto plataforma-projetos

57. **VTX-147** Execução isolada de código gerado por IA (sandbox) → `knowledge/seguranca/sandbox-codigo-ia.md`
58. **VTX-148** Orquestração de LLM: roteamento por modelo, streaming e fallback → `knowledge/engenharia/ia/orquestracao-llm.md`

## F11 — Plataforma de acompanhamento (projeto interno)

59. **VTX-117** Painel Markdown: conexões por projeto e alertas de conexão → `vtx-acompanhamento/painel/conexoes.md`

## F13 — Capacidades para o piloto plataforma-projetos

60. **VTX-149** Medição de tokens, franquia com pausa e chave própria (BYOK) → `knowledge/engenharia/ia/medicao-tokens-byok.md`
61. **VTX-150** Privacidade em IA: retenção zero, não treino e LGPD nos prompts → `knowledge/conformidade/ia-privacidade.md`

## F11 — Plataforma de acompanhamento (projeto interno)

62. **VTX-095** Plataforma: ADR da interface web com acesso restrito → `vtx-acompanhamento/docs/adr/`

## F13 — Capacidades para o piloto plataforma-projetos

63. **VTX-152** Prova de conceito: banco de objetos como camada de trabalho, diff visual e desempenho 3D → `projects/plataforma-projetos/docs/poc/`

## F11 — Plataforma de acompanhamento (projeto interno)

64. **VTX-096** Interface web: estrutura, login restrito e portfólio → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

65. **VTX-153** Importação de arquivos: DWG/DXF só leitura e extração de PDF, DOCX e XLSX → `knowledge/engenharia/importacao-arquivos.md`
66. **VTX-154** Armazenamento de arquivos grandes com custo zero inicial → `knowledge/operacao/armazenamento-arquivos-grandes.md`

## F11 — Plataforma de acompanhamento (projeto interno)

67. **VTX-091** Interface web: atividade dos agentes e handoffs → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

68. **VTX-155** Assinaturas SaaS no Brasil: planos, créditos pré-pagos, Pix e webhooks → `knowledge/engenharia/assinaturas-saas-br.md`
69. **VTX-156** SaaS multi-inquilino: login Google, papéis por disciplina e convites → `knowledge/engenharia/saas-multitenant-auth.md`

## F11 — Plataforma de acompanhamento (projeto interno)

70. **VTX-092** Interface web: fila de aprovações e registro de decisões → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

71. **VTX-157** Comentários no modelo 3D (BCF) e notificações de andamento → `knowledge/engenharia/bim/comentarios-notificacoes.md`
72. **VTX-158** Páginas públicas de portfólio com SEO → `knowledge/engenharia/paginas-publicas-seo.md`

## F11 — Plataforma de acompanhamento (projeto interno)

73. **VTX-118** Interface web: ferramentas e conexões por projeto → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

74. **VTX-159** Quantitativos e memoriais gerados a partir do IFC → `.cursor/skills/ifc-quantitativos/`
75. **VTX-160** Termos de uso, política de privacidade e mapa de dados do piloto → `projects/plataforma-projetos/docs/juridico/`

## F11 — Plataforma de acompanhamento (projeto interno)

76. **VTX-093** Interface web: métricas, custos e alertas → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

77. **VTX-161** Programa alpha com 5 a 10 projetistas → `knowledge/processos/programa-alpha.md`
78. **VTX-162** Captura de dados para fine-tuning futuro (pedido → ação no IFC) → `knowledge/engenharia/ia/dataset-fine-tuning.md`

## F11 — Plataforma de acompanhamento (projeto interno)

79. **VTX-094** Plataforma: uso real por uma semana e decisão continuar ou pivotar → `vtx-acompanhamento/docs/relatorio-mvp.md`

## F13 — Capacidades para o piloto plataforma-projetos

80. **VTX-163** Avaliação de qualidade da IA (evals de modelagem IFC) → `knowledge/engenharia/ia/evals.md`
81. **VTX-164** Inventário das ferramentas Tekto para a v1 (Calc, Docs, Model) → `projects/plataforma-projetos/conhecimento/tekto-ferramentas.md`

## F11 — Plataforma de acompanhamento (projeto interno)

82. **VTX-097** Plataforma: incluir projetos de cliente e outros repositórios → `vtx-acompanhamento/gerador/`

## F13 — Capacidades para o piloto plataforma-projetos

83. **VTX-165** Métricas de produto SaaS (pagantes, churn, custo de IA por projeto) → `knowledge/operacao/metricas-produto-saas.md`

## F8 — Consolidação e validação

84. **VTX-047** Glossário técnico → `knowledge/glossario.md`
85. **VTX-048** Revisão geral da base (consistência, links, fontes) → `knowledge/`
86. **VTX-049** Índice final e guia de navegação para agentes → `knowledge/INDEX.md`
87. **VTX-050** Projeto piloto: definição, triagem do tipo e PRD → `projects/plataforma-projetos/`
88. **VTX-051** Projeto piloto: execução do fluxo completo → `projects/plataforma-projetos/`
89. **VTX-052** Projeto piloto: retrospectiva e ajustes na base → `projects/plataforma-projetos/`
90. **VTX-073** Validação automática do backlog no CI (ids, campos, status, dependências) → `scripts/validar_backlog.py`
91. **VTX-074** Verificação automática de links e fontes da base de conhecimento → `.github/workflows/links.yml`
92. **VTX-075** ROADMAP gerado com status efetivo (só tarefas pendentes) → `scripts/gerar_roadmap.py`

## F10 — Arsenal de scripts e papéis administrativos

93. **VTX-076** Inventário de tarefas recorrentes de desenvolvimento para o arsenal de scripts → `scripts/arsenal/INVENTARIO.md`
94. **VTX-077** Script de estrutura inicial de projeto por tipo → `scripts/arsenal/scaffold.py`
95. **VTX-078** Script de checklist automatizado de revisão de código e qualidade → `scripts/arsenal/revisao.py`
96. **VTX-079** Script de verificações de segurança (dependências e segredos) → `scripts/arsenal/seguranca.py`
97. **VTX-080** Script de verificação de prontidão para deploy → `scripts/arsenal/prontidao_deploy.py`
98. **VTX-081** Skills: receitas curtas que usam o arsenal de scripts → `skills/`
99. **VTX-082** Adotar o formato-fonte de agentes e os exportadores compartilhados → `agentes/`
100. **VTX-083** Papéis administrativos para software house (comercial, financeiro, jurídico e LGPD) → `knowledge/papeis/administrativos/`
