# Avaliação: Graphify

> Fonte: piloto do Tek no [tekto-model](https://github.com/SamAlencar/tekto-model) (18/10/2026). Relatório completo em `/workspace/graphify-piloto/RELATORIO.md` (máquina compartilhada). Pacote PyPI `graphifyy` 0.9.92, Apache-2.0. Build só com AST (tree-sitter), sem LLM.

## Números (estimativa: chars ÷ 4)

| Pergunta | Sem (~tokens) | Com (~tokens) | Economia | Qualidade |
|---|---|---|---|---|
| Q1: onde norma/edição entram no IFC | ~9.900 | ~7.300 | 26% | parcial |
| Q2: o que quebra se `Resultado` mudar | ~14.100 | ~4.700 | **67%** | correto e completo |
| Q3: onde aplicar classificação bSDD | ~3.600 | ~2.000 | 44% | correto |
| **Total** | **~27.600** | **~14.000** | **~49%** | — |

Grafo gerado em ~2 s (136 arquivos → 1510 nós / 3434 arestas). Pasta `graphify-out/` ~5 MB.

## Limites
- O grafo **envelhece a cada commit** — rodar `graphify update` antes de consultar (ou `graphify watch`).
- Nomes comuns geram "Ambiguous" e pedem id completo (1–2 chamadas extras).
- Ganho alto em impacto/chamadas; baixo em perguntas conceituais.
- No tekto-model o repositório é pequeno: economia relativa boa, absoluta modesta.

## Precauções (obrigatórias)
1. Incluir `graphify-out/` no `.gitignore` de qualquer repositório em que for usado.
2. **Nunca** ativar a análise com IA opcional (`GEMINI_API_KEY`). Manter tudo local, só AST.

## Decisão
**Adotado como ferramenta opcional**, só em repositórios grandes, sem integrar aos assistentes (`graphify install`) por enquanto. Uso típico: montar o grafo antes de varrer um repositório de código grande.

## Quando a VTX reutiliza
- Antes de varrer um repositório de código grande (perguntas de "quem chama" / "o que quebra").
- Retestar depois num repositório de código da VTX (o vtx-core é quase documentação; o piloto do Tek já cobre o caso de código).
- Não marcar VTX-125 como concluída só por esta avaliação: a tarefa cobre outras pesquisas da área.
