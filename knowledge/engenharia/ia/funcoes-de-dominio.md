# Funções de domínio para tool-calling da IA

> VTX-146 · 31/10/2026 · Status: padrão adotado para a plataforma-projetos. Código de referência: `core/vtx_ifc/funcoes.py` (testes: `tests/test_funcoes_dominio.py`).

## 1. Por que
Gerar script IfcOpenShell a cada pedido é lento (muitos tokens), difícil de revisar e arriscado de executar. Com funções de domínio a IA só **escolhe uma função e preenche parâmetros JSON**; o código determinístico, testado e versionado faz o resto. Script livre fica como exceção (regra 5 da skill `ifc-python`: processo isolado, nova versão, validação).

| | Script gerado | Função de domínio |
|---|---|---|
| Tokens por pedido | centenas a milhares | dezenas (nome + parâmetros) |
| Revisão | ler código | ler JSON com nomes do domínio |
| Erro | exceção Python crua | `{codigo, campo, mensagem}` que a IA entende e corrige |
| Teste | por pedido, impossível | uma vez, no CI |

Isso também ataca a lentidão de geração que o Samuel apontou: menos saída da IA por pedido, antes de pensar em modelo especializado.

## 2. Contrato
1. **Catálogo** `ferramentas()` → lista `{name, description, input_schema, x-versao-esquema}`; mesmo formato serve à API da Anthropic (`input_schema`), à OpenAI (`parameters`) e a ferramentas MCP (`inputSchema`).
2. **Entrada** em JSON Schema 2020-12, com `additionalProperties: false`, limites (`exclusiveMinimum`, `maximum`) e unidade **no nome do campo** (`altura_mm`). Medidas em mm, como no Revit e nos itens tek TM-262.
3. **Ponto único** `chamar(modelo, nome, args)`: valida o schema → aplica regras de domínio → executa. **Nunca lança exceção** para quem chama.
4. **Saída** `{"ok": true, "resultado": {"GlobalId": ...}}` ou `{"ok": false, "erro": {"codigo", "campo", "mensagem"}}`.
5. **Versão do esquema** (`VERSAO_ESQUEMA`, semver): mudar campo obrigatório ou unidade = versão maior; o histórico da plataforma grava função + versão + args em cada commit (reproduzível).

| Código | Quando | O que a IA faz |
|---|---|---|
| `PARAMETRO_INVALIDO` | fora do schema (tipo, limite, campo faltando ou extra) | corrige o `campo` e repete |
| `ELEMENTO_NAO_ENCONTRADO` | GlobalId não existe ou é de outra classe | lista elementos e escolhe outro |
| `REGRA_VIOLADA` | regra de domínio (vão maior que a parede) | ajusta ou pergunta ao projetista |
| `FUNCAO_DESCONHECIDA` | nome fora do catálogo | consulta `ferramentas()` |
| `ERRO_INTERNO` | bug nosso | para e reporta; não tenta de novo em loop |

## 3. Exemplo (3 funções testadas)
```python
import funcoes as fn
f = fn.receitas.criar_modelo()
p = fn.chamar(f, "criar_parede", {"nome": "P1", "comprimento_mm": 5000, "espessura_mm": 150, "altura_mm": 2800, "externa": True})
fn.chamar(f, "abrir_vao", {"parede": p["resultado"]["GlobalId"], "largura_mm": 900, "altura_mm": 2100, "peitoril_mm": 0, "posicao_mm": 4500})
# {'ok': False, 'erro': {'codigo': 'REGRA_VIOLADA', 'campo': 'posicao_mm', 'mensagem': 'vão termina em 5.400 m, parede tem 5.000 m'}}
fn.chamar(f, "lancar_pilar", {"nome": "C1", "largura_mm": 200, "profundidade_mm": 400, "altura_mm": -1, "x_mm": 0, "y_mm": 0})
# {'ok': False, 'erro': {'codigo': 'PARAMETRO_INVALIDO', 'campo': 'altura_mm', ...}}
```
Os testes conferem também a geometria gerada (pilar 0,2 × 0,4 × 2,8 m) e `ifcopenshell.validate` sem erros.

## 4. Armadilhas encontradas
- **Unidades:** `ifcopenshell.api.*` recebe metro e grava na unidade do arquivo (mm por padrão em `assign_unit`); entidade criada crua (ex.: `IfcRectangleProfileDef`) e leitura de geometria estão na unidade do arquivo. Use `ifcopenshell.util.unit.calculate_unit_scale(f)`. O primeiro rascunho criou pilar de 0,2 mm; o teste de geometria pegou. Corrigido também o comentário errado ("metro") em `receitas.py`.
- **Modo estrito da OpenAI** (structured outputs) exige todos os campos em `required`; campo opcional vira `["boolean", "null"]`. Anthropic e MCP aceitam opcional normal.
- Validar de novo no servidor mesmo com modo estrito: o schema da IA não substitui `chamar()`.
- Regra de domínio ≠ norma: aqui só geometria coerente; verificação normativa vem do tek-calc (TC-126/127) e o projetista revisa e assina.

## 5. Como adicionar uma função
1. Teste falhando em `tests/test_funcoes_dominio.py` (caso ok + um erro de schema + um de regra).
2. Função `_nome(f, args) -> dict` que usa `receitas.py`; erros de domínio via `ErroDominio`.
3. Entrada em `FUNCOES` com `descricao` (uma frase, verbo no imperativo, diz o referencial) e `schema`.
4. Rodar `python -m unittest discover -s tests`; subir `VERSAO_ESQUEMA` se mudou contrato.

## 6. Dependências tek (VTX-F13)
TC-126 (schema JSON estável das ferramentas MCP do tek-calc), TC-127 (catálogo) e TM-261 (exemplos IfcOpenShell como funções) ainda **pendentes** em 31/10. Este padrão foi feito sem eles; quando saírem, as funções de cálculo do tek-calc entram no mesmo catálogo pelo formato acima e TM-261/262 podem substituir `_parede`/`_pilar` por import do tekto-model, sem copiar código.

## 7. Checklist
- [ ] Schema com `additionalProperties: false`, limites e unidade no nome.
- [ ] Erros só pelos 5 códigos; mensagem em pt-BR com valor recebido e limite.
- [ ] Teste de geometria/unidade para função que cria elemento.
- [ ] Função + versão + args gravados no commit do modelo.

## Fontes
- OpenAI, function calling: https://platform.openai.com/docs/guides/function-calling · structured outputs: https://platform.openai.com/docs/guides/structured-outputs
- Anthropic, tool use: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview
- MCP, tools: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- JSON Schema 2020-12: https://json-schema.org/draft/2020-12 · jsonschema (MIT): https://python-jsonschema.readthedocs.io/en/stable/
- IfcOpenShell API 0.9: https://docs.ifcopenshell.org/autoapi/ifcopenshell/api/index.html
