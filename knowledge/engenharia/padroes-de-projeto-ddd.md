# Padrões de projeto e DDD

> VTX-016 · Fase F2 · Base de Conhecimento. Como modelar o **domínio** (DDD) e organizar o **código** (padrões de projeto) nos projetos da VTX. A forma do sistema (estilos, C4, ADRs) está em [Arquitetura de software](arquitetura-de-software.md); os requisitos de entrada, em [Engenharia de requisitos](../processos/engenharia-de-requisitos.md).

## 1. Conceitos essenciais
- **DDD (Domain-Driven Design, Evans):** o código espelha o negócio, com as mesmas palavras do especialista. Tem uma parte **estratégica** (dividir o problema) e uma **tática** (blocos de código).
- **Linguagem ubíqua:** um único vocabulário usado por cliente, PRD, código, testes e agentes. Para agentes é crítico: termo ambíguo vira código errado.
- **Subdomínios:** *núcleo* (o diferencial, merece o melhor desenho), *suporte* (necessário, específico) e *genérico* (comprar/usar pronto: login, e-mail, pagamento).
- **Contexto delimitado** (*bounded context*): fronteira dentro da qual um termo tem um só significado ("Paciente" na agenda ≠ "Paciente" no faturamento). Vira módulo do monólito modular ou, depois, serviço.
- **Padrão de projeto:** solução conhecida para um problema recorrente de código (catálogo GoF). Usar pelo nome ajuda humanos e agentes a se entenderem; usar sem necessidade só complica.

## 2. DDD estratégico (Arquiteto + Produto, etapa de arquitetura)
1. **Glossário:** criar `GLOSSARY.md` no repositório assim que o primeiro termo for decidido. Cada termo: definição de 1–2 frases e `_Evitar_:` sinônimos. Sem detalhe de implementação.
2. **Mapear eventos do negócio** (Event Storming leve): listar em ordem os fatos no passado ("Consulta agendada", "Lembrete enviado"), quem os dispara e as regras entre eles. Pode ser feito pelo agente a partir da entrevista e validado com o cliente.
3. **Agrupar em contextos** e classificar núcleo/suporte/genérico.
4. **Mapa de contextos:** como cada par se relaciona — parceria, cliente-fornecedor, *conformista*, **camada anticorrupção** (tradutor que protege o nosso modelo de um sistema externo/legado), linguagem publicada (contrato OpenAPI/AsyncAPI). Relação entre contextos relevante = ADR.

## 3. DDD tático (Devs, dentro de um contexto)

| Bloco | O que é | Regra prática |
|---|---|---|
| **Entidade** | Tem identidade que dura (Consulta #123) | Igualdade pelo id |
| **Objeto de valor** | Definido só pelos atributos (Horário, CPF, Dinheiro) | Imutável, valida na criação |
| **Agregado** | Grupo tratado como unidade, com uma **raiz** | Só a raiz é acessada de fora; 1 transação = 1 agregado; outros agregados por id |
| **Repositório** | Guarda e busca agregados | Interface no domínio, implementação na infraestrutura |
| **Evento de domínio** | Fato que aconteceu ("ConsultaCancelada") | Integra contextos sem acoplar |
| **Serviço de domínio** | Regra que não cabe numa entidade | Sem estado; nome da linguagem ubíqua |

Organização: regras no **domínio**, sem framework nem banco (núcleo hexagonal); casos de uso na **aplicação**; banco, filas e APIs externas na **infraestrutura**. Preferir **módulos profundos**: interface pequena, testes pela interface.

## 4. Padrões de projeto mais úteis
Usar só quando o problema aparece; citar o nome no código/PR.
- **Criação:** *Factory Method* / *Builder* (montar objetos complexos ou dados de teste).
- **Estrutura:** *Adapter* (integração externa, base da porta-adaptador), *Facade* (interface simples para um subsistema), *Decorator* (log, cache, retentativa sem mexer no original), *Proxy*.
- **Comportamento:** *Strategy* (regras que variam por cliente/plano), *Observer* (eventos), *Command* (fila de ações, desfazer), *State* (status com transições — ex.: pedido), *Chain of Responsibility* (validações/middlewares), *Template Method*.
- **Arquitetura/integração:** Repositório, Unidade de trabalho, Outbox (evento + gravação na mesma transação), Retentativa e *Circuit Breaker* (ver [API e integrações](../processos/fluxos/api-integracoes.md)).

## 5. Quando NÃO usar
- **CRUD simples, site, landing page ou PoC:** camadas simples bastam; DDD tático aqui é custo sem retorno. Manter só glossário.
- **Padrão "por precaução":** uma interface com uma só implementação é seam hipotético; duas implementações (ex.: real + fake de teste) justificam.
- **Agregado gigante:** se uma operação trava muitos objetos, o agregado está grande demais.

## 6. Exemplo
Clínicas (mesmo caso do doc de arquitetura). Contextos: **Agenda** (núcleo), **Cadastro de pacientes** (suporte), **Notificações** (genérico, serviço de e-mail via *Adapter* + camada anticorrupção). Agregado `Agenda` do profissional com raiz que impede conflito de horário; `Horario` é objeto de valor; `ConsultaAgendada` é evento que o contexto Notificações consome via outbox. Regra de lembrete varia por plano → *Strategy*. Glossário: "Consulta" (evitar: atendimento, sessão), "Profissional" (evitar: médico, doutor).

## 7. Checklist
- [ ] `GLOSSARY.md` criado e usado no PRD, código e testes
- [ ] Subdomínios classificados; núcleo identificado
- [ ] Contextos e mapa de contextos; relações relevantes em ADR
- [ ] Agregados pequenos, uma transação por agregado, referência por id
- [ ] Domínio sem dependência de framework/banco; testável sem rede
- [ ] Padrões usados têm motivo e nome citado; nenhum "por precaução"
- [ ] Projeto simples? DDD tático dispensado e isso registrado em `notas`

## Fontes
- Evans, E., *DDD Reference* (2015, CC-BY): https://www.domainlanguage.com/ddd/reference/
- Fowler, M.: *BoundedContext* https://martinfowler.com/bliki/BoundedContext.html · *UbiquitousLanguage* https://martinfowler.com/bliki/UbiquitousLanguage.html · *DDD_Aggregate* https://martinfowler.com/bliki/DDD_Aggregate.html · *ValueObject* https://martinfowler.com/bliki/ValueObject.html
- Microsoft, *Using tactical DDD to design microservices*: https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-ddd
- DDD Crew, *Context Mapping*: https://github.com/ddd-crew/context-mapping · Brandolini, A., *Event Storming*: https://www.eventstorming.com/
- Refactoring.Guru, *Padrões de projeto* (pt-BR): https://refactoring.guru/pt-br/design-patterns
- mattpocock/skills `domain-modeling` (GLOSSARY-FORMAT) e `codebase-design`, pin 49dd158, MIT (em avaliação)
