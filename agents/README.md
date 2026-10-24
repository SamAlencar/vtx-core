# Agentes da VTX

Cada papel terá um arquivo próprio (`agents/<papel>.md`) com: missão, responsabilidades, entradas, saídas (artefatos),
ferramentas permitidas, limites/permissões e critérios de qualidade.

A proposta de papéis (aprovada em 2026-10-10) está em [`knowledge/organizacao/papeis-de-agentes.md`](../knowledge/organizacao/papeis-de-agentes.md).

## Índice

| Agente | Arquivo | Foco |
|---|---|---|
| Orquestrador | [orquestrador.md](orquestrador.md) | Fluxo, backlog, impedimentos |
| Produto | [produto.md](produto.md) | PRD, histórias, prioridades |
| Arquiteto | [arquiteto.md](arquiteto.md) | Arquitetura, ADRs, APIs |
| Dev Backend | [dev-backend.md](dev-backend.md) | APIs, regras de negócio, dados |
| Dev Frontend/Mobile | [dev-frontend-mobile.md](dev-frontend-mobile.md) | Interfaces web e mobile |
| QA | [qa.md](qa.md) | Testes, revisão, aprovação |
| DevOps/SRE | [devops-sre.md](devops-sre.md) | CI/CD, deploy, operação |
| Especialistas | [especialistas.md](especialistas.md) | AppSec, UX/UI, Dados/IA, Docs, Pesquisa |

Modelo:

```markdown
# <Papel>
- Missão:
- Responsabilidades:
- Entradas:
- Saídas (artefatos):
- Ferramentas e permissões:
- Limites (o que NÃO faz):
- Critérios de qualidade / Definition of Done:
- Base de conhecimento a consultar:
```

## Arquétipos (camada ortogonal aos papéis)

Inspirado no post de Boris Cherny (equipe Claude Code, X, out/2026). Cada agente tem um **papel funcional** (acima) e atua em 2–3 **arquétipos** conforme a fase do produto:

| Arquétipo | Foco | Exemplo na VTX |
|---|---|---|
| Prototipador | Muitas ideias rápidas; a maioria não vai para produção | Produto + Dev em PoC descartável |
| Construtor | Transforma protótipo em produto de produção | Devs + Arquiteto |
| Faxineiro | Limpa UI, simplifica código, remove o que não serve, otimiza | QA + Devs (refatoração, performance) |
| Cultivador | Itera para encaixe produto-mercado | Produto + UX + Dados |
| Mantenedor | Seguro, confiável, rápido e eficiente em escala | DevOps/SRE + AppSec |

Mistura por fase (o orquestrador define no início de cada projeto e revisa a cada marco):

| Fase / projeto | Mistura |
|---|---|
| MVP / PoC, piloto | Prototipador + Construtor + Faxineiro |
| med-hub (em construção, pré-PMF) | Construtor + Faxineiro + Prototipador; Cultivador após o 1º incremento em uso |
| Sites (VTX, Tekto, med-hub) | Construtor + Faxineiro + Cultivador (conversão) |
| Produto crescendo | Construtor + Faxineiro + Cultivador + um pouco de Mantenedor |
| Manutenção / produto maduro | Faxineiro + Cultivador + Mantenedor + um pouco de Construtor |

Regra: o arquétipo muda a prioridade, não as permissões do papel. Prototipador nunca publica em produção; protótipo só vira produto pelo Construtor, com testes.
