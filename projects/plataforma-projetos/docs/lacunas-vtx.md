# Lacunas da VTX para construir a plataforma-projetos

Levantamento de 31/10/2026, pedido pelo Samuel, comparando o briefing (`SamAlencar/plataforma-projetos/docs/briefing.md`) com a base da VTX. O que faltava virou a fase **F13 — Capacidades para o piloto** (VTX-143..165). A VTX-051 (execução do piloto) agora depende das tarefas centrais.

| Capacidade | Situação | Tarefas |
|---|---|---|
| Fluxo SaaS, MVP, entrevista, PRD | existe/planejado | VTX-067, 072, 084, 050 |
| Stack, frontend, APIs, dados | planejado | VTX-023..026 |
| Domínio BIM/IFC (IFC4/4x3, IDS, BCF) | ausente | VTX-143 |
| IFC no navegador (That Open, web-ifc) | ausente | VTX-144 |
| IFC no backend (IfcOpenShell 0.9, validação) | ausente | VTX-145 |
| Funções de domínio para tool-calling da IA | ausente | VTX-146 |
| Sandbox para código gerado por IA | ausente | VTX-147 (Docker: VTX-109) |
| Orquestração de LLM (roteamento, streaming) | ausente | VTX-148 |
| Tokens, franquia com pausa, BYOK | ausente | VTX-149 |
| Privacidade em IA (ZDR, não treino) | parcial (LGPD geral: VTX-031) | VTX-150 |
| Versionamento IFC: branches, diff, merge | ausente | VTX-151 |
| PoC diff visual e desempenho 3D | ausente | VTX-152 |
| Importação DWG/DXF/PDF/DOCX/XLSX | ausente | VTX-153 |
| Armazenamento de arquivos grandes grátis | parcial (Supabase: VTX-100) | VTX-154 |
| Assinaturas BR, créditos, Pix | parcial (Stripe/MP: VTX-106) | VTX-155 (Asaas vai ao radar) |
| Multi-inquilino, Google, papéis, convites | parcial (Supabase/auth) | VTX-156 |
| Comentários no 3D e notificações | ausente | VTX-157 |
| Portfólio público e SEO | parcial (frontend: VTX-026) | VTX-158 |
| Quantitativos e memoriais | ausente | VTX-159 |
| Termos, privacidade, mapa de dados | parcial (VTX-031, 083) | VTX-160 (exige Samuel) |
| Programa alpha 5–10 projetistas | ausente | VTX-161 |
| Dados para fine-tuning futuro | ausente | VTX-162 |
| Evals da IA de modelagem | ausente | VTX-163 |
| Inventário das ferramentas Tekto | ausente | VTX-164 |
| Métricas de produto SaaS | parcial (observabilidade: VTX-022) | VTX-165 |

Regras: só ferramentas grátis/open-source; licenças confirmadas com pin (MIT, MPL-2.0, LGPL-3.0 como biblioteca, GPL só como processo separado); sem texto de ABNT ou fonte paga; fichas de ferramentas novas vão para `knowledge/ferramentas/radar.md`.

## Inventário Tekto informado pelo Eng (31/10/2026) — insumo da VTX-164
- Divisão acordada: Tekto = conhecimento de engenharia (funções, cálculo, normas); VTX = plataforma. A plataforma consome os repos tek, não copia.
- tek-calc: MCP, 51 ferramentas NBR 6118, JSON com unidades, ~800 testes → VTX-146, VTX-159.
- tek-docs: Markdown (índices de normas, modelos) → RAG, VTX-159.
- tek-catalog: `tools/ifc_base.py` (IFC4X3_ADD2, mm, tipos, material), `ids_base.py`/`validar.py` (IDS via ifctester) → VTX-145, VTX-146.
- tek-model: exemplos IfcOpenShell (parede, cópia de item), `conhecimento.json`, fluxo de aprovação de mudanças por IA → VTX-143, VTX-151.
- tek-studio: cliente MCP + cartões de proposta auditados; aplicar cartão no IFC (TS-076) pendente → VTX-151.
- Lacunas tek: lajes/vigas/pilares paramétricos, diff de IFC (nenhum repo), quantitativos/preços/4D (D-011 tek-token). Diff de IFC fica com a VTX (VTX-151/152).
- Itens de adaptação tek (empacotar ifc_base, JSON estável no tek-calc, funções paramétricas) aguardam liberação do Samuel; ids tek serão ligados como dependências.
- Decisão de Samuel (31/10): adaptações nos repos tek só depois da VTX. As tarefas F13 não ficam bloqueadas por elas: usam os repos tek como estão (somente leitura) e registram o que precisa mudar como "adaptação tek pós-VTX". Quando a VTX terminar, o Eng cria os itens tek e passa os ids.
