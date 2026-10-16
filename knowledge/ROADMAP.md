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
8. **VTX-072** Fluxo de projeto: MVP / prova de conceito → `knowledge/processos/fluxos/mvp-poc.md`
9. **VTX-011** Engenharia de requisitos → `knowledge/processos/engenharia-de-requisitos.md`
10. **VTX-012** Scrum e Kanban adaptados a agentes → `knowledge/processos/scrum-kanban-agentes.md`
11. **VTX-013** Operação de agentes: prompts, contexto e memória → `knowledge/processos/operacao-de-agentes.md`
12. **VTX-014** Governança e aprovações (humano no circuito) → `knowledge/processos/governanca-e-aprovacoes.md`

## F2 — Engenharia de software

13. **VTX-015** Arquitetura de software (estilos, C4, ADRs) → `knowledge/engenharia/arquitetura-de-software.md`
14. **VTX-016** Padrões de projeto e DDD → `knowledge/engenharia/padroes-de-projeto-ddd.md`
15. **VTX-017** Padrões de código, Clean Code e code review → `knowledge/engenharia/padroes-de-codigo.md`
16. **VTX-018** Estratégia de testes e qualidade → `knowledge/engenharia/testes-e-qualidade.md`
17. **VTX-019** Git e CI/CD → `knowledge/engenharia/git-e-ci-cd.md`

## F3 — Segurança e operação

18. **VTX-020** Segurança no desenvolvimento (OWASP, SSDF) → `knowledge/seguranca/desenvolvimento-seguro.md`
19. **VTX-021** DevOps e SRE (IaC, SLOs, incidentes) → `knowledge/operacao/devops-sre.md`
20. **VTX-022** Observabilidade (logs, métricas, traces) → `knowledge/operacao/observabilidade.md`

## F4 — Tecnologia e plataformas

21. **VTX-023** Stack de referência da VTX → `knowledge/tecnologia/stack-de-referencia.md`
22. **VTX-024** Design de APIs → `knowledge/tecnologia/design-de-apis.md`
23. **VTX-025** Modelagem de dados e bancos de dados → `knowledge/tecnologia/modelagem-de-dados.md`
24. **VTX-026** Desenvolvimento frontend web → `knowledge/tecnologia/frontend-web.md`
25. **VTX-027** Desenvolvimento mobile → `knowledge/tecnologia/mobile.md`
26. **VTX-028** UX/UI e acessibilidade → `knowledge/tecnologia/ux-ui-acessibilidade.md`

## F5 — Gestão e conformidade

27. **VTX-029** Gestão de projetos, riscos e comunicação com cliente → `knowledge/gestao/gestao-de-projetos.md`
28. **VTX-030** Estimativas e planejamento → `knowledge/gestao/estimativas.md`
29. **VTX-031** LGPD e compliance → `knowledge/seguranca/lgpd-compliance.md`
30. **VTX-032** Documentação técnica (docs-as-code) → `knowledge/gestao/documentacao-tecnica.md`

## F6 — Templates de artefatos

31. **VTX-033** Template de PRD → `knowledge/templates/prd.md`
32. **VTX-034** Template de história de usuário e critérios de aceite → `knowledge/templates/historia-de-usuario.md`
33. **VTX-035** Template de ADR → `knowledge/templates/adr.md`
34. **VTX-036** Template de plano e relatório de testes → `knowledge/templates/plano-de-testes.md`
35. **VTX-037** Template de runbook e postmortem → `knowledge/templates/runbook-postmortem.md`
36. **VTX-038** Template de relatório diário e de sprint → `knowledge/templates/relatorios.md`

## F7 — Diretrizes por papel

37. **VTX-039** Diretrizes do agente Orquestrador → `knowledge/diretrizes/orquestrador.md`
38. **VTX-040** Diretrizes do agente Produto → `knowledge/diretrizes/produto.md`
39. **VTX-041** Diretrizes do agente Arquiteto → `knowledge/diretrizes/arquiteto.md`
40. **VTX-042** Diretrizes do agente Dev Backend → `knowledge/diretrizes/dev-backend.md`
41. **VTX-043** Diretrizes do agente Dev Frontend/Mobile → `knowledge/diretrizes/dev-frontend-mobile.md`
42. **VTX-044** Diretrizes do agente QA → `knowledge/diretrizes/qa.md`
43. **VTX-045** Diretrizes do agente DevOps/SRE → `knowledge/diretrizes/devops-sre.md`
44. **VTX-046** Diretrizes dos especialistas sob demanda → `knowledge/diretrizes/especialistas.md`

## F9 — Integração com o Cursor e operação

45. **VTX-053** AGENTS.md raiz com diretrizes gerais dos agentes → `AGENTS.md`
46. **VTX-054** Regra sempre ativa: fluxo entre papéis, DoD e aprovações → `.cursor/rules/vtx-base.mdc`
47. **VTX-055** Regras por papel: Orquestrador, Produto e Arquiteto → `.cursor/rules/papeis/planejamento.mdc`
48. **VTX-056** Regras por papel: Devs, QA e DevOps/SRE → `.cursor/rules/papeis/execucao.mdc`
49. **VTX-057** Regras por assunto com globs: testes e APIs → `.cursor/rules/assuntos/testes-api.mdc`
50. **VTX-058** Regras por assunto com globs: frontend/mobile e segurança → `.cursor/rules/assuntos/frontend-seguranca.mdc`
51. **VTX-059** Estratégia de consulta sob demanda e índice para agentes → `knowledge/index.yaml`
52. **VTX-060** Template de repositório de projeto → `templates/projeto/`
53. **VTX-061** Sincronização de regras e script de bootstrap de projetos → `scripts/bootstrap_projeto.sh`
54. **VTX-062** Ambiente dos agentes de nuvem (environment.json, segredos, permissões) → `.cursor/environment.json`
55. **VTX-063** Orquestração com issues, PRs e agentes de nuvem por papel e tipo de projeto → `knowledge/processos/orquestracao-cursor.md`
56. **VTX-064** Pontos de aprovação do Samuel (branch protegida, revisões, release) → `knowledge/processos/pontos-de-aprovacao.md`
57. **VTX-065** Teste de validação da integração com o Cursor → `projects/validacao-cursor/`

## F8 — Consolidação e validação

58. **VTX-047** Glossário técnico → `knowledge/glossario.md`
59. **VTX-048** Revisão geral da base (consistência, links, fontes) → `knowledge/`
60. **VTX-049** Índice final e guia de navegação para agentes → `knowledge/INDEX.md`
61. **VTX-050** Projeto piloto: definição, triagem do tipo e PRD → `projects/piloto/`
62. **VTX-051** Projeto piloto: execução do fluxo completo → `projects/piloto/`
63. **VTX-052** Projeto piloto: retrospectiva e ajustes na base → `projects/piloto/`
64. **VTX-073** Validação automática do backlog no CI (ids, campos, status, dependências) → `scripts/validar_backlog.py`
65. **VTX-074** Verificação automática de links e fontes da base de conhecimento → `.github/workflows/links.yml`
66. **VTX-075** ROADMAP gerado com status efetivo (só tarefas pendentes) → `scripts/gerar_roadmap.py`

## F10 — Arsenal de scripts e papéis administrativos

67. **VTX-076** Inventário de tarefas recorrentes de desenvolvimento para o arsenal de scripts → `scripts/arsenal/INVENTARIO.md`
68. **VTX-077** Script de estrutura inicial de projeto por tipo → `scripts/arsenal/scaffold.py`
69. **VTX-078** Script de checklist automatizado de revisão de código e qualidade → `scripts/arsenal/revisao.py`
70. **VTX-079** Script de verificações de segurança (dependências e segredos) → `scripts/arsenal/seguranca.py`
71. **VTX-080** Script de verificação de prontidão para deploy → `scripts/arsenal/prontidao_deploy.py`
72. **VTX-081** Skills: receitas curtas que usam o arsenal de scripts → `skills/`
73. **VTX-082** Adotar o formato-fonte de agentes e os exportadores compartilhados → `agentes/`
74. **VTX-083** Papéis administrativos para software house (comercial, financeiro, jurídico e LGPD) → `knowledge/papeis/administrativos/`
