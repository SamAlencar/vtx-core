# med-hub (4med.co)

Plataforma chat-first para médicos PJ (3 MCPs), implementada pelos agentes da VTX **em paralelo ao piloto plataforma-projetos** (decisão do Samuel, 20/10/2026).

- Fonte única de verdade do planejamento: [SamAlencar/4medco-base-conhecimento](https://github.com/SamAlencar/4medco-base-conhecimento) (importado de `planejamento/vtx/`, commit 0da4cba, preparado pelo Bil).
- [PRD](docs/produto/PRD.md) · [ADRs](docs/adr/) · [Pesquisa de domínio](conhecimento/pesquisa-dominio.md)
- Aprovação de escopo (A2): 18/10/2026.
- ADR-0002 (Supabase) está **proposto**, sujeito à VTX-023 (stack de referência).

## Pendências
- Issues por história (HU-xx, épicos A–G) só depois das convenções de issues/PRs da F9.
- Reformatar quando existirem os templates oficiais (knowledge/templates/).
- Incremento 5 depende da base contábil (prevista até 12/11/2026); incremento 6 depende de uma base jurídica ainda não planejada.

## Incrementos (ordem sugerida)
1. Base segura (HU-01, 02, 04) · 2. Assinatura e onboarding (HU-03, 06, 07, 08) · 3. Parceiro contábil e consultas (HU-22, 10, 14, 09, 12) · 4. Assistente e MCP da plataforma (HU-21, 15, 11, 20) · 5. MCP contábil (HU-13) · 6. Jurídico (HU-16, 17, 23) · 7. Seguros, comunicação e admin (HU-18, 19, 24, 25, 05)
