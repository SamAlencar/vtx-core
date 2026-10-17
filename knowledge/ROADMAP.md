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

## F5 — Gestão e conformidade

28. **VTX-029** Gestão de projetos, riscos e comunicação com cliente → `knowledge/gestao/gestao-de-projetos.md`
29. **VTX-030** Estimativas e planejamento → `knowledge/gestao/estimativas.md`
30. **VTX-031** LGPD e compliance → `knowledge/seguranca/lgpd-compliance.md`
31. **VTX-032** Documentação técnica (docs-as-code) → `knowledge/gestao/documentacao-tecnica.md`

## F6 — Templates de artefatos

32. **VTX-033** Template de PRD → `knowledge/templates/prd.md`
33. **VTX-034** Template de história de usuário e critérios de aceite → `knowledge/templates/historia-de-usuario.md`
34. **VTX-035** Template de ADR → `knowledge/templates/adr.md`
35. **VTX-036** Template de plano e relatório de testes → `knowledge/templates/plano-de-testes.md`
36. **VTX-037** Template de runbook e postmortem → `knowledge/templates/runbook-postmortem.md`
37. **VTX-038** Template de relatório diário e de sprint → `knowledge/templates/relatorios.md`

## F7 — Diretrizes por papel

38. **VTX-039** Diretrizes do agente Orquestrador → `knowledge/diretrizes/orquestrador.md`
39. **VTX-040** Diretrizes do agente Produto → `knowledge/diretrizes/produto.md`
40. **VTX-041** Diretrizes do agente Arquiteto → `knowledge/diretrizes/arquiteto.md`
41. **VTX-042** Diretrizes do agente Dev Backend → `knowledge/diretrizes/dev-backend.md`
42. **VTX-043** Diretrizes do agente Dev Frontend/Mobile → `knowledge/diretrizes/dev-frontend-mobile.md`
43. **VTX-044** Diretrizes do agente QA → `knowledge/diretrizes/qa.md`
44. **VTX-045** Diretrizes do agente DevOps/SRE → `knowledge/diretrizes/devops-sre.md`
45. **VTX-046** Diretrizes dos especialistas sob demanda → `knowledge/diretrizes/especialistas.md`

## F9 — Integração com o Cursor e operação

46. **VTX-053** AGENTS.md raiz com diretrizes gerais dos agentes → `AGENTS.md`
47. **VTX-054** Regra sempre ativa: fluxo entre papéis, DoD e aprovações → `.cursor/rules/vtx-base.mdc`
48. **VTX-055** Regras por papel: Orquestrador, Produto e Arquiteto → `.cursor/rules/papeis/planejamento.mdc`
49. **VTX-056** Regras por papel: Devs, QA e DevOps/SRE → `.cursor/rules/papeis/execucao.mdc`
50. **VTX-057** Regras por assunto com globs: testes e APIs → `.cursor/rules/assuntos/testes-api.mdc`
51. **VTX-058** Regras por assunto com globs: frontend/mobile e segurança → `.cursor/rules/assuntos/frontend-seguranca.mdc`
52. **VTX-059** Estratégia de consulta sob demanda e índice para agentes → `knowledge/index.yaml`
53. **VTX-060** Template de repositório de projeto → `templates/projeto/`
54. **VTX-061** Sincronização de regras e script de bootstrap de projetos → `scripts/bootstrap_projeto.sh`
55. **VTX-062** Ambiente dos agentes de nuvem (environment.json, segredos, permissões) → `.cursor/environment.json`
56. **VTX-063** Orquestração com issues, PRs e agentes de nuvem por papel e tipo de projeto → `knowledge/processos/orquestracao-cursor.md`
57. **VTX-064** Pontos de aprovação do Samuel (branch protegida, revisões, release) → `knowledge/processos/pontos-de-aprovacao.md`
58. **VTX-065** Teste de validação da integração com o Cursor → `projects/validacao-cursor/`

## F11 — Plataforma de acompanhamento (projeto interno)

59. **VTX-085** Planejamento da plataforma de acompanhamento → `knowledge/projetos-internos/plataforma-acompanhamento.md`
60. **VTX-086** Plataforma: PRD do MVP, hipóteses e critérios de sucesso → `vtx-acompanhamento/docs/prd-mvp.md`
61. **VTX-087** Formatos de registro: eventos, handoffs, decisões e custos → `registro/ + backlog/SCHEMA.md`
62. **VTX-088** Formato da fila de aprovações do Samuel → `registro/aprovacoes.yaml + backlog/SCHEMA.md`
63. **VTX-089** Gerador de dados da plataforma (JSON privado único) → `vtx-acompanhamento/gerador/`
64. **VTX-090** Painel privado: portfólio, fases e progresso → `vtx-acompanhamento/painel/`
65. **VTX-091** Painel privado: atividade dos agentes e handoffs → `vtx-acompanhamento/painel/agentes.md`
66. **VTX-092** Painel privado: fila de aprovações e registro de decisões → `vtx-acompanhamento/painel/aprovacoes.md`
67. **VTX-093** Painel privado: métricas, custos e alertas no resumo diário → `vtx-acompanhamento/painel/metricas.md`
68. **VTX-094** Plataforma: uso real por uma semana e decisão continuar ou pivotar → `vtx-acompanhamento/docs/relatorio-mvp.md`
69. **VTX-095** Plataforma: ADR da interface web com acesso restrito → `vtx-acompanhamento/docs/adr/`
70. **VTX-096** Plataforma: interface web interativa sobre o mesmo JSON → `vtx-acompanhamento/web/`
71. **VTX-097** Plataforma: incluir projetos de cliente e outros repositórios → `vtx-acompanhamento/gerador/`

## F8 — Consolidação e validação

72. **VTX-047** Glossário técnico → `knowledge/glossario.md`
73. **VTX-048** Revisão geral da base (consistência, links, fontes) → `knowledge/`
74. **VTX-049** Índice final e guia de navegação para agentes → `knowledge/INDEX.md`
75. **VTX-050** Projeto piloto: definição, triagem do tipo e PRD → `projects/piloto/`
76. **VTX-051** Projeto piloto: execução do fluxo completo → `projects/piloto/`
77. **VTX-052** Projeto piloto: retrospectiva e ajustes na base → `projects/piloto/`
78. **VTX-073** Validação automática do backlog no CI (ids, campos, status, dependências) → `scripts/validar_backlog.py`
79. **VTX-074** Verificação automática de links e fontes da base de conhecimento → `.github/workflows/links.yml`
80. **VTX-075** ROADMAP gerado com status efetivo (só tarefas pendentes) → `scripts/gerar_roadmap.py`

## F10 — Arsenal de scripts e papéis administrativos

81. **VTX-076** Inventário de tarefas recorrentes de desenvolvimento para o arsenal de scripts → `scripts/arsenal/INVENTARIO.md`
82. **VTX-077** Script de estrutura inicial de projeto por tipo → `scripts/arsenal/scaffold.py`
83. **VTX-078** Script de checklist automatizado de revisão de código e qualidade → `scripts/arsenal/revisao.py`
84. **VTX-079** Script de verificações de segurança (dependências e segredos) → `scripts/arsenal/seguranca.py`
85. **VTX-080** Script de verificação de prontidão para deploy → `scripts/arsenal/prontidao_deploy.py`
86. **VTX-081** Skills: receitas curtas que usam o arsenal de scripts → `skills/`
87. **VTX-082** Adotar o formato-fonte de agentes e os exportadores compartilhados → `agentes/`
88. **VTX-083** Papéis administrativos para software house (comercial, financeiro, jurídico e LGPD) → `knowledge/papeis/administrativos/`
