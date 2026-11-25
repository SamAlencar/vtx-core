# Fluxo de projeto: sistema web / plataforma SaaS

> VTX-067 · Fase F1 · Base de Conhecimento. Especializa o [SOP entre agentes](../fluxo-entre-agentes.md) para sistemas web e plataformas SaaS. Vale quando a [triagem](triagem.md) define `tipo_principal: sistema-web-saas` (fluxo padrão quando nenhuma das 5 perguntas de decisão dá "sim").

## 1. Conceitos
- **Sistema web:** aplicação acessada pelo navegador, com login, regras de negócio e banco de dados (ex.: gestão interna de uma empresa).
- **SaaS (Software como Serviço):** sistema web vendido a vários clientes (*tenants*) por assinatura. Acrescenta três preocupações: **isolamento entre clientes**, **cobrança** e **operação contínua** (AWS SaaS Lens).
- **Modelo de tenancy:** *silo* (banco/infra por cliente), *pool* (tudo compartilhado, separado por `tenant_id`) ou *bridge* (misto). A escolha é uma decisão de arquitetura (ADR) e afeta custo, segurança e LGPD.
- **Incremento entregável:** fatia vertical (tela + API + banco + teste) que um usuário consegue usar. Preferir fatias a camadas.
- **Doze fatores:** configuração por variáveis de ambiente, processos sem estado, logs como fluxo, paridade entre ambientes. Base para deploy simples e escalável.
- **Ferramentas:** padrão — GitHub Actions, Cursor, Cloudflare, Supabase, Stripe, Sentry, Docker, Figma. Opcional — Vercel, Appwrite, Firebase, Google + Grok Bot. Detalhe na [matriz ferramenta × fluxo](../../ferramentas/README.md#matriz); a escolha formal fica no [stack de referência](../../tecnologia/stack-de-referencia.md) e no ADR.

## 2. Etapas do fluxo

| # | Etapa | Papéis | Artefatos | Portão |
|---|---|---|---|---|
| 0 | Triagem | Orquestrador | `projects/<p>/ficha.yaml` | Tipo confirmado |
| 1 | Descoberta e requisitos | Produto (+ UX) | PRD, personas, mapa de histórias, **matriz de perfis e permissões**, requisitos não funcionais (desempenho, disponibilidade, LGPD) | **Samuel aprova escopo e MVP** |
| 2 | UX/UI | UX/UI Designer | Fluxos de tela e protótipo das jornadas principais; guia visual mínimo (WCAG 2.2 AA) | Produto valida contra histórias |
| 3 | Arquitetura | Arquiteto (+ Segurança) | Diagramas C4 (contexto e contêineres), modelo de dados, contrato OpenAPI, ADRs: stack, autenticação, tenancy, hospedagem | Revisão do Orquestrador; Segurança obrigatória (há dados de usuários) |
| 4 | Fundação | DevOps + Dev Backend | Repositório, CI (lint, testes, build), ambientes dev/homologação/produção, IaC, autenticação e esqueleto multi-tenant, observabilidade básica | Deploy automático em homologação funcionando |
| 5 | Incrementos | Devs Backend/Frontend + QA | Issues pequenas → PRs com testes; relatório de QA por incremento | CI verde, critérios de aceite, revisão independente |
| 6 | Endurecimento | QA + Segurança + DevOps | Testes E2E das jornadas críticas, checagem OWASP Top 10/ASVS nível 1–2, teste de carga simples, backup e restauração testados | Sem falha crítica ou alta aberta |
| 7 | Lançamento | DevOps + Orquestrador | Notas de versão, runbook, SLOs definidos, plano de rollback, termos de uso e política de privacidade revisados | **Samuel aprova produção** |
| 8 | Operação e evolução | DevOps/SRE + Produto | Monitoramento, alertas, incidentes, métricas de uso; novas demandas entram pelo fluxo de [manutenção](manutencao-evolucao.md) | Retrospectiva registrada |

As etapas 5 e 6 repetem por incremento. Cada incremento termina publicado em homologação para o Samuel ver.

## 3. Pontos de aprovação do Samuel
1. Escopo e corte do MVP (etapa 1).
2. Escolhas com custo recorrente: hospedagem, serviços pagos, gateway de cobrança (etapa 3).
3. Tratamento de dados pessoais: base legal, retenção, operadores (etapa 3, com Segurança).
4. Cada publicação em produção (etapa 7) e mudanças de preço/plano no SaaS.

## 4. Itens específicos de SaaS (pular se for sistema de um único cliente)
- `tenant_id` em toda tabela e consulta; teste automatizado que tenta ler dado de outro cliente e precisa falhar.
- Cadastro self-service, convite de usuários, papéis por tenant.
- Planos, limites e cobrança recorrente (integração de pagamento entra como módulo [API e integrações](api-integracoes.md)).
- Painel administrativo interno (suporte, suspensão de conta) com trilha de auditoria.
- Exportação e exclusão de dados do cliente (direitos do titular, LGPD art. 18).

## 5. Riscos típicos e mitigação

| Risco | Mitigação |
|---|---|
| Escopo cresce sem controle | MVP aprovado por escrito; novas ideias vão ao backlog, não ao incremento atual |
| Vazamento entre tenants | ADR de tenancy, filtro central por `tenant_id`, teste de isolamento no CI |
| Falha de autenticação/autorização | Usar provedor ou biblioteca consolidada; matriz de permissões testada; ASVS |
| Ambiente "só funciona na máquina do agente" | Doze fatores, IaC, homologação idêntica à produção |
| Lentidão com dados reais | Índices revisados no modelo de dados, paginação, teste de carga na etapa 6 |
| Custo de nuvem acima do previsto | Estimativa no ADR de hospedagem, alerta de orçamento |

## 6. Exemplo
"Sistema de agendamento para clínicas, vendido por assinatura." Etapa 1: 3 perfis (admin, recepção, profissional), 14 histórias, MVP = agenda + cadastro de pacientes; Samuel aprova. Etapa 3: ADR-003 tenancy *pool* com `tenant_id`; dados de saúde marcam Segurança e LGPD. Etapa 4: CI e homologação no ar em 2 dias. Etapa 5: 3 incrementos (agenda, pacientes, lembretes). Etapa 6: teste de isolamento acha consulta sem filtro; corrigida. Etapa 7: Samuel aprova produção; SLO de 99,5% de disponibilidade mensal.

## 7. Checklist de conclusão
- [ ] PRD, matriz de permissões e MVP aprovados pelo Samuel
- [ ] C4, modelo de dados, OpenAPI e ADRs (stack, auth, tenancy, hospedagem) salvos
- [ ] CI/CD e três ambientes funcionando; configuração fora do código
- [ ] Jornadas críticas com teste E2E; isolamento entre tenants testado (se SaaS)
- [ ] OWASP Top 10/ASVS verificados; sem falha crítica ou alta
- [ ] Backup e restauração testados; monitoramento, alertas e SLOs ativos
- [ ] Privacidade e termos revisados; produção aprovada pelo Samuel
- [ ] Runbook, notas de versão e retrospectiva registrados


## Recursos por papel
Áreas deste fluxo: frontend e design, backend e APIs, testes e QA, segurança, MCP, documentação. Fonte: [recursos.yaml](../../ferramentas/recursos.yaml) (narrativa em [bibliotecas-e-recursos.md](../../ferramentas/bibliotecas-e-recursos.md)). Usar só o que está **adotado**, listado nas seções dos agentes [Frontend/Mobile](../../../agents/dev-frontend-mobile.md), [Backend](../../../agents/dev-backend.md), [QA](../../../agents/qa.md), [DevOps/SRE](../../../agents/devops-sre.md), [Arquiteto](../../../agents/arquiteto.md), [Especialistas](../../../agents/especialistas.md). Em avaliação não entra no incremento sem piloto. Se esta página e o YAML divergirem, vale o YAML.

## Fontes
- AWS, *Well-Architected SaaS Lens* (modelos silo/pool/bridge, isolamento): https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html
- Wiggins, A., *The Twelve-Factor App*: https://12factor.net/pt_br/
- Brown, S., *The C4 model for visualising software architecture*: https://c4model.com/
- OWASP, *Top 10*: https://owasp.org/Top10/ e *ASVS*: https://owasp.org/www-project-application-security-verification-standard/
- W3C, *WCAG 2.2*: https://www.w3.org/TR/WCAG22/
- Google, *SRE Book — Service Level Objectives*: https://sre.google/sre-book/service-level-objectives/
- DORA, *Trunk-based development*: https://dora.dev/capabilities/trunk-based-development/
- Brasil, Lei nº 13.709/2018 (LGPD): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
