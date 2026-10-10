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
