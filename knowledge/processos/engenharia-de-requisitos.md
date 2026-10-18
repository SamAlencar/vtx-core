# Engenharia de requisitos

> VTX-011 · Fase F1 · Base de Conhecimento. Como a VTX descobre, escreve, valida e mantém requisitos. Vale para todos os fluxos (VTX-066 a 072). A entrevista com o cliente ([entrevista-cliente.md](fluxos/entrevista-cliente.md)) é a principal fonte de entrada; este documento cobre o que vem depois dela até o PRD aprovado e durante o projeto.

## 1. Conceitos
- **Requisito:** necessidade ou condição que o sistema deve atender, escrita de forma verificável (ISO/IEC/IEEE 29148).
- **Níveis:** *negócio* (por que o projeto existe, metas e métricas) → *usuário* (o que cada perfil precisa fazer) → *sistema* (comportamento e qualidades do software).
- **Funcional:** o que o sistema faz (ex.: "agendar consulta").
- **Não funcional (atributo de qualidade):** como faz: desempenho, segurança, usabilidade, disponibilidade, manutenibilidade etc. Usar as características da ISO/IEC 25010 como lista de verificação.
- **Restrição:** decisão já tomada que limita a solução (prazo, orçamento, stack, LGPD, só ferramentas gratuitas).
- **Premissa:** algo tido como verdadeiro sem prova; vira risco se falhar.
- **Critério de aceite:** condição objetiva que diz se uma história está pronta.
- **Rastreabilidade:** ligação objetivo → requisito → issue/PR → teste.

## 2. Atividades (ciclo contínuo)

| # | Atividade | Dono | Entrada | Saída |
|---|---|---|---|---|
| 1 | Elicitação | Produto (+ Orquestrador) | Ficha de triagem, entrevista, documentos e sistemas existentes | Notas brutas, glossário inicial |
| 2 | Análise | Produto + Arquiteto | Notas | Requisitos classificados, conflitos e lacunas listados, prioridade (MoSCoW) |
| 3 | Especificação | Produto | Requisitos analisados | PRD + histórias com critérios de aceite + NFRs mensuráveis |
| 4 | Validação | QA + Arquiteto, depois Samuel | PRD | PRD revisado; **aprovação do Samuel (escopo)** |
| 5 | Gestão | Orquestrador | PRD aprovado, pedidos de mudança | PRD versionado, registro de mudanças, rastreabilidade |

Técnicas de elicitação por situação: entrevista (padrão), análise de documentos e do sistema atual (manutenção), observação de tela/gravação do processo, protótipo de baixa fidelidade (quando o cliente "só sabe quando vê"), oficina tipo Lean Inception (vários interessados).

## 3. Como escrever

**História de usuário** (Cohn), com critérios INVEST (independente, negociável, valiosa, estimável, pequena, testável):
```
Como <perfil>, quero <ação> para <benefício>.
```

**Critérios de aceite** em Gherkin (viram teste automatizado pelo QA):
```gherkin
Cenário: horário já ocupado
  Dado que o horário 10h de 20/11 está reservado
  Quando o paciente tenta reservar 10h de 20/11
  Então o sistema recusa e sugere os 3 horários livres mais próximos
```

**Requisito de sistema** no padrão EARS (frases curtas e sem ambiguidade):
- Ubíquo: "O sistema deve registrar data e autor de cada alteração no agendamento."
- Por evento: "Quando um agendamento for cancelado, o sistema deve notificar o profissional em até 1 minuto."
- Indesejado: "Se o pagamento falhar, então o sistema deve manter a reserva por 15 minutos."

**Não funcionais sempre com número e forma de medir** (nada de "rápido" ou "seguro"):
"95% das buscas respondem em até 500 ms com 100 usuários simultâneos (teste de carga k6)."

**Boas qualidades de um requisito** (29148): necessário, sem ambiguidade, verificável, viável, consistente, completo e rastreável. Palavras proibidas sem número: *rápido, fácil, intuitivo, flexível, robusto, etc., e/ou, adequado*.

## 4. Estrutura mínima do PRD
1. Contexto e problema · 2. Objetivos e métricas de sucesso · 3. Perfis de usuário · 4. Escopo (dentro / fora) · 5. Histórias com critérios de aceite, priorizadas (MoSCoW) · 6. Requisitos não funcionais (checklist ISO 25010) · 7. Restrições e premissas · 8. Dados pessoais tratados e base legal (LGPD) · 9. Riscos e dúvidas em aberto · 10. Glossário · 11. Histórico de versões.

Salvar em `docs/produto/PRD.md` no repositório do projeto. Um PRD por projeto; histórias grandes viram épicos com histórias filhas.

## 5. Regras específicas para agentes
- **Não inventar requisito.** Lacuna vira pergunta registrada em "Dúvidas em aberto", nunca suposição silenciosa. Toda afirmação do PRD cita a fonte (trecho da entrevista, documento, decisão do Samuel).
- **Separar fato de sugestão.** Ideias do agente vão marcadas como *proposta* até o cliente aceitar.
- **Revisão cruzada.** Quem escreve (Produto) não valida sozinho: QA verifica testabilidade, Arquiteto verifica viabilidade e NFRs.
- **Contexto enxuto.** O agente de implementação recebe só a história, os critérios e os NFRs que a afetam, não o PRD inteiro.
- **Rastreabilidade leve:** cada issue cita o id da história (ex.: `HU-07`); cada PR cita a issue; cada teste de aceite leva o id no nome.

## 6. Gestão de mudanças
1. Pedido novo entra como item no PRD com status *proposto*.
2. Produto avalia impacto (escopo, prazo, arquitetura, custo); Arquiteto opina se mexe em decisão registrada (ADR).
3. Mudança de escopo ou prazo → **aprovação do Samuel**; ajuste de detalhe dentro do escopo → Produto decide e registra.
4. Atualizar versão do PRD e histórico; avisar os agentes afetados pela passagem padrão (SOP).

## 7. Exemplo curto
Entrevista do sistema de agendamento: cliente diz "o sistema tem que ser rápido e não deixar marcar em cima". Produto escreve `HU-03 Como paciente, quero ver só horários livres para não ter conflito`, com o cenário Gherkin acima, e o NFR "listagem de horários em até 500 ms (p95)". A dúvida "pode haver encaixe de urgência?" fica em aberto e vai para o cliente. QA confirma que o critério é testável; Samuel aprova o escopo v1.0.

## 8. Checklist
- [ ] Objetivos de negócio com métrica de sucesso
- [ ] Perfis de usuário definidos
- [ ] Escopo dentro / fora explícito
- [ ] Toda história com critério de aceite testável (Gherkin)
- [ ] NFRs com número e forma de medir (revisados contra ISO 25010)
- [ ] Restrições, premissas e dados pessoais (LGPD) registrados
- [ ] Nenhuma suposição sem fonte; dúvidas em aberto listadas
- [ ] Revisado por QA e Arquiteto; aprovado pelo Samuel
- [ ] PRD versionado; issues citam os ids das histórias

## Fontes
- ISO/IEC/IEEE 29148:2018, *Requirements engineering*: https://www.iso.org/standard/72089.html
- IEEE Computer Society, *SWEBOK Guide v4.0* (2024), cap. Software Requirements: https://www.computer.org/education/bodies-of-knowledge/software-engineering
- IREB, *CPRE Foundation Level* (sílabo): https://www.ireb.org/en/cpre/foundation/
- Wiegers, K.; Beatty, J. *Software Requirements*, 3ª ed. (2013).
- Cohn, M. *User Stories Applied* (2004).
- Wake, B. *INVEST in Good Stories* (2003): https://xp123.com/invest-in-good-stories-and-smart-tasks/
- Mavin, A. et al. *EARS: Easy Approach to Requirements Syntax* (2009): https://alistairmavin.com/ears/
- Cucumber, *Gherkin Reference*: https://cucumber.io/docs/gherkin/reference/
- ISO/IEC 25010:2023, *Product quality model*: https://www.iso.org/standard/78176.html
- Lei 13.709/2018 (LGPD): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
