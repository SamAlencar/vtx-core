# Fluxo de projeto: manutenção e evolução de sistema existente

> VTX-071 · Fase F1 · Base de Conhecimento. Especializa o [SOP entre agentes](../fluxo-entre-agentes.md) para sistemas que já estão em produção (nossos ou de terceiros). Vale quando a [triagem](triagem.md) define `tipo_principal: manutencao-evolucao`; o fluxo do tipo original ([SaaS](sistema-web-saas.md), [app](app-mobile.md), [API](api-integracoes.md), [site](site-landing-page.md)) entra como módulo técnico.

## 1. Conceitos
- **Tipos de manutenção (ISO/IEC/IEEE 14764):** *corretiva* (bug), *adaptativa* (mudança de ambiente: SO, lib, lei, API externa), *perfectiva* (nova função, desempenho, UX) e *preventiva* (dívida técnica, atualização de dependências, refatoração).
- **Primeiro entender, depois mudar:** em código herdado, o risco está no que ninguém documentou. O diagnóstico vem antes de qualquer estimativa firme.
- **Testes de caracterização:** testes que registram o comportamento *atual* (certo ou errado) antes de alterar o código; viram rede de segurança (Feathers).
- **Mudança pequena e reversível:** PRs curtos, feature flags, rollback testado. Substituição grande é gradual (padrão *Strangler Fig*), nunca reescrita "big bang".
- **Linha de base:** métricas medidas antes da mudança (erros, latência, uso) para provar que a entrega melhorou e nada regrediu.
- **Ferramentas:** padrão — GitHub Actions, Cursor, Sentry. As demais (Supabase, Appwrite, Firebase, Expo, Stripe, Vercel, Cloudflare, Docker, Figma) só entram se o sistema já as usa, ou na mudança aprovada por ADR. Detalhe na [matriz ferramenta × fluxo](../../ferramentas/README.md#matriz).

## 2. Etapas do fluxo

| # | Etapa | Papéis | Artefatos | Portão |
|---|---|---|---|---|
| 0 | Triagem | Orquestrador | `projects/<p>/ficha.yaml`, tipo de manutenção e urgência | `tipo_principal: manutencao-evolucao` |
| 1 | Acesso e inventário | DevOps + Arquiteto | Lista de acessos (repo, ambientes, logs), stack, dependências, como fazer build e deploy | **Samuel aprova acessos e confidencialidade** |
| 2 | Diagnóstico | Arquiteto + Dev + QA | Relatório de diagnóstico: arquitetura atual, riscos, cobertura de testes, dívida, CVEs, linha de base de métricas | Revisão do Orquestrador |
| 3 | Plano e estimativa | Produto + Arquiteto | Backlog priorizado por valor x risco, ADRs das mudanças relevantes, estimativa por item | **Samuel aprova plano e custo** |
| 4 | Rede de segurança | DevOps + QA | CI reproduzível, testes de caracterização nas áreas tocadas, ambiente de staging, backup e rollback testados | Build e testes verdes no estado atual |
| 5 | Incrementos | Dev + QA | Um item por PR, com flag quando arriscado; changelog e versão (SemVer) | CI verde, aceite, revisão independente |
| 6 | Verificação | QA + Segurança | Regressão, comparação com a linha de base, varredura de dependências | Sem regressão nem falha crítica/alta aberta |
| 7 | Release | DevOps + Orquestrador | Notas de versão, janela de deploy, plano de rollback, comunicação ao cliente | **Samuel aprova release em produção** |
| 8 | Operação contínua | DevOps + Produto | Monitoramento, postmortem de incidentes, ciclo preventivo (dependências, CVEs) | Retrospectiva e relatório periódico registrados |

Bug urgente em produção (*hotfix*) segue atalho: 0 → diagnóstico curto → 4 mínimo (teste que reproduz o bug) → 5 → 7. A documentação completa vem depois, no postmortem.

## 3. Pontos de aprovação do Samuel
1. Acesso a código, dados e ambientes do cliente, inclusive termo de confidencialidade (etapa 1).
2. Plano, prioridades e custo, depois do diagnóstico (etapa 3). Estimativa antes do diagnóstico é só faixa.
3. Mudanças irreversíveis: migração de dados, troca de stack ou de fornecedor pago (ADR na etapa 3).
4. Cada release em produção e todo hotfix fora da janela combinada (etapa 7).

## 4. Itens específicos de manutenção
- **Dados reais:** nunca copiar produção para dev sem anonimizar; logs e dumps com dado pessoal seguem a LGPD.
- **Dependências:** inventário com versão e fim de suporte; atualização em lotes pequenos, com Dependabot/Renovate e análise de vulnerabilidades (OWASP A06).
- **Código de terceiros:** sem testes nem documentação, o diagnóstico registra "áreas desconhecidas", e o plano reserva tempo para elas.
- **Compatibilidade:** mudança em API ou banco preserva contratos (versão nova, migração expand/contract); clientes da API são avisados antes.
- **Métricas:** acompanhar DORA (frequência de deploy, lead time, taxa de falha de mudança, tempo de recuperação) e o orçamento de erro do serviço.
- **Documentação viva:** cada intervenção atualiza o README de execução, os ADRs e o changelog; o próximo agente não pode depender de memória.

## 5. Riscos típicos e mitigação

| Risco | Mitigação |
|---|---|
| Regressão em parte não testada | Testes de caracterização antes de mexer; PR pequeno; staging |
| Estimativa estoura por código desconhecido | Diagnóstico pago/curto antes do plano; estimativa em faixa |
| Deploy quebra sem volta | Rollback ensaiado, backup verificado, feature flag |
| Reescrita total que nunca termina | Strangler Fig: substituir módulo a módulo com valor em cada etapa |
| Dependência sem suporte ou com CVE | Inventário, varredura no CI, ciclo preventivo mensal |
| Conhecimento só na cabeça do dev anterior | Sessão de handover, registro no diagnóstico e no README |

## 6. Exemplo
"Sistema de pedidos de um cliente, feito por outra empresa, está lento e precisa emitir NF-e." Etapa 1: Samuel aprova acesso ao repositório e ao banco de homologação. Etapa 2: diagnóstico mostra consulta sem índice, PHP fora de suporte e zero testes. Etapa 3: plano em três itens (índice, atualização do PHP, integração NF-e como módulo [API e integrações](api-integracoes.md)); Samuel aprova. Etapa 4: testes de caracterização no fluxo de pedido. Etapa 5: índice primeiro (p95 de 4 s para 300 ms frente à linha de base), depois PHP, depois NF-e atrás de flag. Etapa 7: Samuel aprova cada release.

## 7. Checklist de conclusão
- [ ] Acessos e confidencialidade aprovados pelo Samuel; inventário salvo
- [ ] Relatório de diagnóstico com riscos, dívida, CVEs e linha de base
- [ ] Plano e custo aprovados; ADRs das mudanças relevantes
- [ ] CI reproduzível, testes de caracterização, backup e rollback testados
- [ ] Cada mudança em PR pequeno, revisado, com changelog e versão
- [ ] Regressão e comparação com a linha de base sem piora
- [ ] Release aprovada pelo Samuel; cliente comunicado
- [ ] Monitoramento ativo, postmortems e retrospectiva registrados

## Fontes
- ISO/IEC/IEEE 14764:2022, *Software engineering — Software life cycle processes — Maintenance* (categorias de manutenção).
- IEEE Computer Society, *SWEBOK Guide*, capítulo "Software Maintenance": https://www.computer.org/education/bodies-of-knowledge/software-engineering
- Michael Feathers, *Working Effectively with Legacy Code* (Prentice Hall, 2004) · *Characterization test*: https://en.wikipedia.org/wiki/Characterization_test
- Martin Fowler, *Strangler Fig Application*: https://martinfowler.com/bliki/StranglerFigApplication.html · Pete Hodgson, *Feature Toggles*: https://martinfowler.com/articles/feature-toggles.html
- DORA, *DORA's software delivery metrics*: https://dora.dev/guides/dora-metrics-four-keys/
- Google, *SRE Book* — *Embracing Risk*: https://sre.google/sre-book/embracing-risk/ · *Postmortem Culture*: https://sre.google/sre-book/postmortem-culture/
- OWASP Top 10, *A06 Vulnerable and Outdated Components*: https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/ · GitHub, *Dependabot*: https://docs.github.com/en/code-security/dependabot
- *Versionamento Semântico*: https://semver.org/lang/pt-BR/ · *Keep a Changelog*: https://keepachangelog.com/pt-BR/1.1.0/ · *Architectural Decision Records*: https://adr.github.io/
- Brasil, Lei nº 13.709/2018 (LGPD): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
