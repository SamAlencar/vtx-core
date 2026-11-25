# Especialistas sob demanda

Ativados pelo Orquestrador conforme o projeto (modelo *enabling team*). Ver [Papéis de agentes](../knowledge/organizacao/papeis-de-agentes.md).

| Especialista | Quando ativar | Entrega principal | Conhecimento ([ROADMAP](../knowledge/ROADMAP.md)) |
|---|---|---|---|
| Segurança (AppSec) | Projetos com dados pessoais; antes de cada release | Modelagem de ameaças, revisão SAST/SCA, parecer de release | VTX-020 Segurança, VTX-031 LGPD |
| UX/UI Designer | Interface nova ou design system | Fluxos, protótipos, design system | VTX-028 UX/UI e acessibilidade |
| Dados / IA | Analytics, ML ou LLM | Pipelines de dados, modelos, componente "como serviço" | VTX-025 Bancos de dados |
| Documentação Técnica | Entrega ao cliente, APIs públicas | Manuais, docs de API, guias | VTX-024 Design de APIs |
| Pesquisador | Contínuo, um tema do ROADMAP por sessão | Novo documento em `knowledge/` | [ROADMAP](../knowledge/ROADMAP.md) |

Definições completas serão criadas quando o especialista for ativado pela primeira vez.
- **Recursos por papel:** áreas segurança, frontend, UI e design, documentação. Fonte: [recursos.yaml](../knowledge/ferramentas/recursos.yaml) (detalhe em [bibliotecas-e-recursos.md](../knowledge/ferramentas/bibliotecas-e-recursos.md)). Só o que está **adotado** entra no trabalho do dia a dia; em avaliação fica no catálogo até o piloto ou a revisão periódica. Se o YAML e esta lista divergirem, vale o YAML.

| Área | Recurso | Id |
|---|---|---|
| frontend, UI e design | [Impeccable](https://github.com/pbakaus/impeccable) | `impeccable` |
| frontend, UI e design | [shadcn/ui](https://github.com/shadcn-ui/ui) | `shadcn-ui` |
| segurança | [OWASP Cheat Sheet Series](https://github.com/OWASP/CheatSheetSeries) | `owasp-cheatsheets` |
| frontend, UI e design | [Tailwind CSS](https://github.com/tailwindlabs/tailwindcss) | `tailwind-css` |
| frontend, UI e design | [Radix Primitives](https://github.com/radix-ui/primitives) | `radix-primitives` |
| frontend, UI e design | [axe-core](https://github.com/dequelabs/axe-core) | `axe-core` |
| frontend, UI e design | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | `wcag-22` |
| frontend, UI e design | [WAI-ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/) | `wai-aria-apg` |
| segurança | [gitleaks](https://github.com/gitleaks/gitleaks) | `gitleaks` |
| segurança | [Semgrep Community Edition](https://github.com/semgrep/semgrep) | `semgrep-ce` |
| segurança | [OSV-Scanner](https://github.com/google/osv-scanner) | `osv-scanner` |
| documentação | [Skill de diagramas editoriais (VTX)](https://github.com/cathrynlavery/diagram-design) | `diagramas-editoriais` |
