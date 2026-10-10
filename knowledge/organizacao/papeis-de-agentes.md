# Papéis de agentes da VTX

> Área: Organização · Versão: v1 (proposta) · Data: 2026-10-10 · Status: aguardando aprovação

## 1. Conceitos

- **Papel = conjunto de responsabilidades (accountabilities), não cargo.** O Scrum Guide 2020 trocou "papéis" por
  *accountabilities*: Product Owner (valor do produto e backlog), Scrum Master (eficácia do time) e Developers
  (incremento com qualidade, segundo a Definition of Done) [1][2]. Para agentes, isso significa: cada agente tem um
  escopo claro de **o que entrega** e **pelo que responde**.
- **Especialização + artefatos estruturados.** Frameworks multiagente de software (MetaGPT, ChatDev) mostram que
  agentes com papéis especializados que se comunicam por **documentos padronizados** (PRD, design, lista de tarefas,
  testes) produzem resultados mais consistentes e com menos alucinação do que conversa livre [3][4].
  O MetaGPT modela uma empresa com Product Manager, Arquiteto, Gerente de Projeto, Engenheiro e QA [3].
- **Carga cognitiva limitada.** Team Topologies organiza times em quatro tipos (stream-aligned, platform, enabling,
  complicated-subsystem) para reduzir a carga cognitiva de quem entrega valor [5]. Para agentes, "carga cognitiva"
  é a **janela de contexto e o custo em tokens**: cada agente deve carregar só o conhecimento do seu papel.
- **Segurança e operação são responsabilidades explícitas**, não etapas finais: o NIST SSDF integra segurança a
  todo o ciclo (preparar, proteger, produzir, responder) [6]; a SRE do Google trata confiabilidade como a principal
  característica do produto (SLOs, monitoramento, resposta a incidentes) [7]; DORA mede desempenho de entrega
  (frequência de deploy, lead time, taxa de falha, tempo de restauração) [8].

## 2. Metodologia — proposta de estrutura

Princípio: **começar enxuto** (núcleo de 7 agentes) e ativar especialistas sob demanda. O humano (Samuel) é o
**patrocinador/aprovador**: define objetivos, aprova escopo, releases e gastos.

### 2.1 Núcleo (sempre ativo)

| # | Agente | Base nas boas práticas | Responsabilidades principais | Artefatos de saída |
|---|---|---|---|---|
| 1 | **Orquestrador (Gerente de Projeto / Scrum Master)** | Scrum Master [1]; Project Manager do MetaGPT [3] | Decompor trabalho, distribuir tarefas, manter o backlog diário, remover impedimentos, garantir o fluxo e a DoD | `backlog/AAAA-MM-DD.yaml`, relatórios diários |
| 2 | **Produto (Product Owner / Analista de Requisitos)** | Product Owner [1]; Product Manager [3] | Entender o cliente, escrever PRD, histórias e critérios de aceite, priorizar o backlog de produto | PRD, histórias de usuário |
| 3 | **Arquiteto de Software** | Architect [3]; complicated-subsystem [5] | Desenho do sistema, escolha de stack, interfaces, modelo de dados, ADRs; revisão técnica | Documento de arquitetura, ADRs, contratos de API |
| 4 | **Desenvolvedor Backend** | Developers [1]; Engineer [3] | APIs, regras de negócio, banco de dados, testes unitários | Código + testes |
| 5 | **Desenvolvedor Frontend/Mobile** | Developers [1] | Interfaces web e mobile, integração com APIs, acessibilidade | Código + testes |
| 6 | **QA (Engenheiro de Qualidade)** | QA Engineer [3]; tester/reviewer do ChatDev [4] | Plano de testes, testes automatizados (unitários, integração, E2E), validação dos critérios de aceite, code review independente | Plano e relatório de testes |
| 7 | **DevOps / SRE** | SRE [7]; DORA [8]; platform team [5] | CI/CD, infraestrutura como código, ambientes, deploy, monitoramento, SLOs, resposta a incidentes | Pipelines, IaC, runbooks |

### 2.2 Especialistas (ativados sob demanda — modelo "enabling team" [5])

| Agente | Quando ativar | Base |
|---|---|---|
| **Segurança (AppSec)** | Todo projeto com dados de usuários; revisão antes de cada release | NIST SSDF [6] |
| **UX/UI Designer** | Projetos com interface nova ou design system | — |
| **Dados / IA** | Projetos com analytics, ML ou LLM | complicated-subsystem [5] |
| **Documentação Técnica** | Entrega ao cliente, APIs públicas | — |
| **Pesquisador (Base de Conhecimento)** | Contínuo, uma sessão por tema do `ROADMAP.md` | — |

### 2.3 Fluxo padrão (SOP)

```
Cliente/Samuel → Produto (PRD) → Arquiteto (design/ADRs) → Orquestrador (tarefas)
   → Devs (código+testes) → QA (validação) → Segurança (se aplicável) → DevOps (deploy)
   → Orquestrador (registro no backlog → painel)
```

Cada passagem de bastão é feita por **artefato versionado no repositório**, não por conversa solta [3].

### 2.4 Regras de governança

1. **Separação de funções:** quem escreve o código não aprova sozinho — QA (e Segurança quando aplicável) revisa.
2. **Mínimo privilégio:** cada agente só acessa as ferramentas do seu papel (ex.: só DevOps faz deploy) [6].
3. **Humano no circuito:** aprovação do Samuel para escopo, releases em produção, custos e comunicação externa.
4. **Contexto mínimo:** cada agente carrega apenas seu `agents/<papel>.md` e os documentos de conhecimento citados nele.

## 3. Exemplos

- **App simples de agendamento:** Produto → Arquiteto → 1 Backend + 1 Frontend → QA → DevOps. Segurança revisa
  antes do lançamento (dados pessoais / LGPD).
- **Correção de bug em produção:** Orquestrador abre a tarefa → Dev corrige com teste de regressão → QA valida →
  DevOps faz deploy e registra o incidente (postmortem sem culpados [7]).
- **Projeto com IA embarcada:** núcleo + agente Dados/IA como complicated-subsystem, fornecendo o componente
  como serviço ao time [5].

## 4. Checklist

- [ ] Cada agente tem missão, entradas, saídas, ferramentas e limites definidos em `agents/<papel>.md`
- [ ] Toda tarefa tem um único agente responsável no backlog
- [ ] Nenhum código vai para produção sem revisão de QA
- [ ] Segurança é acionada em projetos com dados pessoais
- [ ] Artefatos de cada etapa ficam versionados no repositório
- [ ] Métricas DORA acompanhadas a partir do primeiro projeto
- [ ] Samuel aprova escopo e releases

## 5. Próximos passos

1. Samuel aprova/ajusta a lista de papéis.
2. Criar `agents/<papel>.md` para os 7 papéis do núcleo.
3. Próximo tema de pesquisa: fluxo de trabalho entre agentes (SOP detalhado) — ver `ROADMAP.md`.

## Fontes

1. Schwaber & Sutherland — *The Scrum Guide* (2020). https://scrumguides.org/scrum-guide.html
2. Scrum.org — *Scrum Guide 2020 Update: Role to Accountabilities*. https://www.scrum.org/resources/blog/scrum-guide-2020-update-role-accountabilities
3. Hong et al. — *MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework* (ICLR 2024). https://arxiv.org/abs/2308.00352
4. Qian et al. — *ChatDev: Communicative Agents for Software Development* (ACL 2024). https://arxiv.org/abs/2307.07924
5. Team Topologies — *Key concepts*. https://teamtopologies.com/key-concepts · Martin Fowler — https://martinfowler.com/bliki/TeamTopologies.html
6. NIST SP 800-218 — *Secure Software Development Framework (SSDF) v1.1*. https://csrc.nist.gov/pubs/sp/800/218/final
7. Google — *Site Reliability Engineering* (livro). https://sre.google/sre-book/preface/
8. Google Cloud — *DORA / Four Key metrics*. https://cloud.google.com/blog/products/devops-sre/supercharge-your-devops-practice-with-sre-principles
