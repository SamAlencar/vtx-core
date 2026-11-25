# Roadmap da Base de Conhecimento

Gerado por `scripts/gerar_roadmap.py` a partir do status efetivo do backlog (mestre + diários).
Só entram tarefas ainda não concluídas nem canceladas, em ordem de prioridade. Próxima: `python scripts/proxima_tarefa.py`.
Ao concluir um documento, adicioná-lo ao `INDEX.md`.

## F14 — Primeiros clientes

1. **VTX-196** med-hub: incremento 1 interno, com prazo e teto de esforço → `projects/med-hub/docs/plano.md`
2. **VTX-197** med-hub: tarefas de entrega e repositório do piloto → `backlog/projeto.yaml`
3. **VTX-204** Build técnico do site da VTX → `projects/site-vtx/README.md`
4. **VTX-199** Pacote técnico de manutenção, SLA e suporte → `knowledge/operacao/suporte-e-sla.md`
5. **VTX-200** Módulos reutilizáveis extraídos do med-hub → `templates/web-next/modulos/`
6. **VTX-201** Template de site/landing → `templates/site/`
7. **VTX-202** Template de API → `templates/api/`
8. **VTX-203** Template de app Expo (só quando houver cliente de app) → `templates/app-expo/`
9. **VTX-205** Retrospectiva por projeto alimentando a base → `knowledge/templates/retrospectiva.md`
10. **VTX-208** Tratar o alerta de npm audit do template web-next (postcss no Next) → `templates/web-next/package-lock.json`
11. **VTX-209** CI do vtx-core rodar o pipeline npm do template web → `.github/workflows/testes.yml`

## F1 — Processo e operação de agentes

12. **VTX-172** Revisão obrigatória antes do merge (auditoria P0 item 6) → `.github/pull_request_template.md + .github/CODEOWNERS + knowledge/processos/governanca-e-aprovacoes.md`
13. **VTX-174** Human-in-the-loop verificável (evidência de aprovação A2) → `backlog/SCHEMA.md + scripts/validar_backlog.py`

## F9 — Integração com o Cursor e operação

14. **VTX-210** Regras do Cursor de engenharia e de agentes no template web → `templates/web-next/.cursor/rules/`

## F13 — Capacidades para o piloto plataforma-projetos

15. **VTX-212** Fronteira de camadas imposta por lint no template web → `templates/web-next/eslint.config.mjs`
16. **VTX-177** Harness de agente de referência (loop de tool-calling) → `core/agente/loop.py + tests/test_loop_agente.py + knowledge/engenharia/ia/orquestracao-llm.md`

## F9 — Integração com o Cursor e operação

17. **VTX-224** Deny rules do Cursor e segredos fora do contexto do agente → `.cursor/cli.json`

## F5 — Gestão e conformidade

18. **VTX-029** Gestão de projetos, riscos e comunicação com cliente → `knowledge/gestao/gestao-de-projetos.md`

## F12 — Catálogo de ferramentas

19. **VTX-186** A/B do mapa Trail-code e decisão sobre o MCP → `knowledge/ferramentas/piloto-trail-code.md`

## F5 — Gestão e conformidade

20. **VTX-030** Estimativas e planejamento → `knowledge/gestao/estimativas.md`

## F13 — Capacidades para o piloto plataforma-projetos

21. **VTX-178** Suíte de evals mínima com portão no CI → `evals/README.md + evals/executar.py + knowledge/engenharia/ia/evals.md`

## F5 — Gestão e conformidade

22. **VTX-031** LGPD e compliance → `knowledge/seguranca/lgpd-compliance.md`

## F13 — Capacidades para o piloto plataforma-projetos

23. **VTX-179** Log estruturado por execução de agente e custo → `core/agente/telemetria.py + knowledge/operacao/observabilidade.md`

## F1 — Processo e operação de agentes

24. **VTX-225** Proteção real da branch main (ruleset ou hook de pre-push) → `.githooks/pre-push`

## F8 — Consolidação e validação

25. **VTX-181** Lint de código e de Markdown no CI (ruff e markdownlint) → `pyproject.toml + .markdownlint.json + .github/workflows/testes.yml`

## F1 — Processo e operação de agentes

26. **VTX-214** Portão de merge sem proteção de branch → `scripts/mesclar_pr.sh`

## F9 — Integração com o Cursor e operação

27. **VTX-188** Remover a cópia redundante das regras de tokens em knowledge/templates/cursor → `knowledge/templates/cursor/README.md`

## F8 — Consolidação e validação

28. **VTX-215** Lint e tipos em Python no CI → `pyproject.toml`

## F6 — Templates de artefatos

29. **VTX-034** Template de história de usuário e critérios de aceite → `knowledge/templates/historia-de-usuario.md`

## F9 — Integração com o Cursor e operação

30. **VTX-189** Bootstrap criar docs/memoria/ no repositório do cliente → `scripts/bootstrap_projeto.sh + templates/projeto/docs/memoria/`

## F3 — Segurança e operação

31. **VTX-190** Levar o pre-commit com gitleaks ao template de projeto → `templates/projeto/.pre-commit-config.yaml`

## F8 — Consolidação e validação

32. **VTX-183** Exemplo ponta a ponta de agente rodando (onboarding) → `projects/exemplo-agente/`

## F3 — Segurança e operação

33. **VTX-191** Validar o hook pre-commit de gitleaks no CI → `.github/workflows/testes.yml`

## F13 — Capacidades para o piloto plataforma-projetos

34. **VTX-192** Validar IDS com XSD local, sem baixar schema pela rede → `core/vtx_ifc/`

## F6 — Templates de artefatos

35. **VTX-038** Template de relatório diário e de sprint → `knowledge/templates/relatorios.md`

## F9 — Integração com o Cursor e operação

36. **VTX-206** Enriquecer AGENTS.md e regras por papel só quando o uso real mostrar lacuna → `AGENTS.md + .cursor/rules/papeis/`

## F7 — Diretrizes por papel

37. **VTX-207** Detalhar agents/*.md quando um projeto real mostrar a lacuna → `agents/`

## F9 — Integração com o Cursor e operação

38. **VTX-057** Regras por assunto com globs: testes e APIs → `.cursor/rules/assuntos/testes-api.mdc`
39. **VTX-058** Regras por assunto com globs: frontend/mobile e segurança → `.cursor/rules/assuntos/frontend-seguranca.mdc`
40. **VTX-138** Regras comuns e por stack em .cursor/rules a partir do ECC → `.cursor/rules/ (common-*, typescript, react, react-native, python) e knowledge/templates/cursor/`
41. **VTX-139** Hooks do Cursor como guardrails locais (adaptados do ECC) → `.cursor/hooks.json e scripts/hooks/ (padrão TT-060)`
42. **VTX-060** Template de repositório de projeto → `templates/projeto/`
43. **VTX-061** Sincronização de regras e script de bootstrap de projetos → `scripts/bootstrap_projeto.sh`
44. **VTX-062** Ambiente dos agentes de nuvem (environment.json, segredos, permissões) → `.cursor/environment.json`

## F3 — Segurança e operação

45. **VTX-187** Migrar a documentação de med-hub e plataforma-projetos para os repositórios dos produtos → `projects/med-hub/README.md + projects/plataforma-projetos/README.md`

## F9 — Integração com o Cursor e operação

46. **VTX-063** Orquestração com issues, PRs e agentes de nuvem por papel e tipo de projeto → `knowledge/processos/orquestracao-cursor.md`
47. **VTX-064** Pontos de aprovação do Samuel (branch protegida, revisões, release) → `knowledge/processos/pontos-de-aprovacao.md`

## F11 — Plataforma de acompanhamento (projeto interno)

48. **VTX-086** Plataforma: PRD do MVP, hipóteses e critérios de sucesso → `vtx-acompanhamento/docs/prd-mvp.md`
49. **VTX-087** Formatos de registro: eventos, handoffs, decisões e custos → `registro/ + backlog/SCHEMA.md`
50. **VTX-088** Formato da fila de aprovações do Samuel → `registro/aprovacoes.yaml + backlog/SCHEMA.md`
51. **VTX-115** Esquema do manifesto de conexões por projeto → `projects/CONEXOES.md + projects/<p>/conexoes.yaml`
52. **VTX-089** Gerador de dados da plataforma (JSON privado único) → `vtx-acompanhamento/gerador/`
53. **VTX-116** Verificador de status das conexões (somente leitura) → `vtx-acompanhamento/verificador/`
54. **VTX-090** Painel Markdown (semana 1): portfólio, fases e progresso → `vtx-acompanhamento/painel/`

## F13 — Capacidades para o piloto plataforma-projetos

55. **VTX-147** Execução isolada de código gerado por IA (sandbox) → `knowledge/seguranca/sandbox-codigo-ia.md`
56. **VTX-148** Orquestração de LLM: roteamento por modelo, streaming e fallback → `knowledge/engenharia/ia/orquestracao-llm.md`

## F11 — Plataforma de acompanhamento (projeto interno)

57. **VTX-117** Painel Markdown: conexões por projeto e alertas de conexão → `vtx-acompanhamento/painel/conexoes.md`

## F13 — Capacidades para o piloto plataforma-projetos

58. **VTX-149** Medição de tokens, franquia com pausa e chave própria (BYOK) → `knowledge/engenharia/ia/medicao-tokens-byok.md`
59. **VTX-150** Privacidade em IA: retenção zero, não treino e LGPD nos prompts → `knowledge/conformidade/ia-privacidade.md`

## F11 — Plataforma de acompanhamento (projeto interno)

60. **VTX-095** Plataforma: ADR da interface web com acesso restrito → `vtx-acompanhamento/docs/adr/`

## F13 — Capacidades para o piloto plataforma-projetos

61. **VTX-152** Prova de conceito: banco de objetos como camada de trabalho, diff visual e desempenho 3D → `projects/plataforma-projetos/docs/poc/`

## F11 — Plataforma de acompanhamento (projeto interno)

62. **VTX-096** Interface web: estrutura, login restrito e portfólio → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

63. **VTX-153** Importação de arquivos: DWG/DXF só leitura e extração de PDF, DOCX e XLSX → `knowledge/engenharia/importacao-arquivos.md`
64. **VTX-154** Armazenamento de arquivos grandes com custo zero inicial → `knowledge/operacao/armazenamento-arquivos-grandes.md`

## F11 — Plataforma de acompanhamento (projeto interno)

65. **VTX-091** Interface web: atividade dos agentes e handoffs → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

66. **VTX-155** Assinaturas SaaS no Brasil: planos, créditos pré-pagos, Pix e webhooks → `knowledge/engenharia/assinaturas-saas-br.md`
67. **VTX-156** SaaS multi-inquilino: login Google, papéis por disciplina e convites → `knowledge/engenharia/saas-multitenant-auth.md`

## F11 — Plataforma de acompanhamento (projeto interno)

68. **VTX-092** Interface web: fila de aprovações e registro de decisões → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

69. **VTX-157** Comentários no modelo 3D (BCF) e notificações de andamento → `knowledge/engenharia/bim/comentarios-notificacoes.md`
70. **VTX-158** Páginas públicas de portfólio com SEO → `knowledge/engenharia/paginas-publicas-seo.md`

## F11 — Plataforma de acompanhamento (projeto interno)

71. **VTX-118** Interface web: ferramentas e conexões por projeto → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

72. **VTX-159** Quantitativos e memoriais gerados a partir do IFC → `.cursor/skills/ifc-quantitativos/`
73. **VTX-160** Termos de uso, política de privacidade e mapa de dados do piloto → `projects/plataforma-projetos/docs/juridico/`

## F11 — Plataforma de acompanhamento (projeto interno)

74. **VTX-093** Interface web: métricas, custos e alertas → `vtx-acompanhamento/web/`

## F13 — Capacidades para o piloto plataforma-projetos

75. **VTX-161** Programa alpha com 5 a 10 projetistas → `knowledge/processos/programa-alpha.md`
76. **VTX-162** Captura de dados para fine-tuning futuro (pedido → ação no IFC) → `knowledge/engenharia/ia/dataset-fine-tuning.md`

## F11 — Plataforma de acompanhamento (projeto interno)

77. **VTX-094** Plataforma: uso real por uma semana e decisão continuar ou pivotar → `vtx-acompanhamento/docs/relatorio-mvp.md`

## F13 — Capacidades para o piloto plataforma-projetos

78. **VTX-163** Avaliação de qualidade da IA (evals de modelagem IFC) → `knowledge/engenharia/ia/evals.md`
79. **VTX-164** Inventário das ferramentas Tekto para a v1 (Calc, Docs, Model) → `projects/plataforma-projetos/conhecimento/tekto-ferramentas.md`

## F11 — Plataforma de acompanhamento (projeto interno)

80. **VTX-097** Plataforma: incluir projetos de cliente e outros repositórios → `vtx-acompanhamento/gerador/`

## F13 — Capacidades para o piloto plataforma-projetos

81. **VTX-165** Métricas de produto SaaS (pagantes, churn, custo de IA por projeto) → `knowledge/operacao/metricas-produto-saas.md`

## F8 — Consolidação e validação

82. **VTX-050** Projeto piloto: definição, triagem do tipo e PRD → `projects/plataforma-projetos/`
83. **VTX-051** Projeto piloto: execução do fluxo completo → `projects/plataforma-projetos/`
84. **VTX-052** Projeto piloto: retrospectiva e ajustes na base → `projects/plataforma-projetos/`

## F10 — Arsenal de scripts e papéis administrativos

85. **VTX-076** Inventário de tarefas recorrentes de desenvolvimento para o arsenal de scripts → `scripts/arsenal/INVENTARIO.md`
86. **VTX-078** Script de checklist automatizado de revisão de código e qualidade → `scripts/arsenal/revisao.py`
87. **VTX-079** Script de verificações de segurança (dependências e segredos) → `scripts/arsenal/seguranca.py`
88. **VTX-080** Script de verificação de prontidão para deploy → `scripts/arsenal/prontidao_deploy.py`
89. **VTX-081** Skills: receitas curtas que usam o arsenal de scripts → `skills/`
90. **VTX-083** Papéis administrativos para software house (comercial, financeiro, jurídico e LGPD) → `knowledge/papeis/administrativos/`
