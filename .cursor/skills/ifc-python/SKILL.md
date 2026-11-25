---
name: ifc-python
description: Use ao ler, criar, editar ou validar arquivos IFC no backend em Python (IfcOpenShell 0.9 + ifctester/IDS), inclusive para gerar a nova versão (commit) de um modelo a partir de um script da IA ou comparar duas versões por GlobalId.
---

# IFC no backend (IfcOpenShell 0.9)

O código vive no pacote `vtx_ifc` (`core/vtx_ifc/`, `pip install -e .`). Receitas em `vtx_ifc.receitas` (testes: `tests/test_ifc_python.py`, rodam no CI). Domínio (esquemas, Psets, IDS): `projects/plataforma-projetos/conhecimento/bim-ifc.md`.

## Instalação (grátis, LGPL-3.0, só como biblioteca)
`pip install -e .` na raiz do vtx-core (puxa IfcOpenShell 0.9.0.post1 e ifctester 0.9.0, PyPI, Python 3.12+). Não modificar nem redistribuir a biblioteca alterada; usar por import mantém o código da VTX livre de LGPL.

## Receitas
| Tarefa | Função | Observação |
|---|---|---|
| Modelo novo | `criar_modelo(schema="IFC4")` | Projeto, unidade do arquivo mm (a API recebe metro e converte), contexto Body, Site/Edifício/Pavimento. Para infraestrutura use `"IFC4X3_ADD2"`. |
| Parede | `criar_parede(f, nome, comp, esp, alt, psets)` | `IfcWall` (não `IfcWallStandardCase`, obsoleta no IFC4); valida medidas > 0. |
| Listar | `listar(f, "IfcWall")` | Funciona em IFC2X3, IFC4 e IFC4X3; `by_type` inclui subclasses. |
| Psets | `ler_psets(e)` / `definir_pset(f, e, {...})` | Elemento sem Pset devolve `{}`; herda do tipo. |
| Validar | `validar_ids(ifc, ids)` | IDS 1.0 via ifctester; devolve `aprovado` + falhas por especificação (JSON). Exemplo: `vtx_ifc/exemplo.ids`. |
| Tool-calling | `funcoes.chamar(f, nome, args)` / `funcoes.ferramentas()` | Funções de domínio com JSON Schema e erro estruturado (VTX-146); entrada em mm. |
| Comparar | `diff_por_globalid(a, b)` | Adicionados/removidos/alterados (classe, nome, Psets; não geometria). Base da VTX-151. |

## Camada de objetos (VTX-152)
`vtx_ifc.objetos`: `extrair(f)` gera um objeto JSON por elemento (globalid, classe, nome, tipo, psets, qtos, materiais, andar, grupos) para Postgres `jsonb` e para a IA; `aplicar(f, objetos)` devolve ao IFC base só o que mudou (nome, psets, andar, grupos, tipo), nunca cria elemento e nunca lança (erros `globalid_inexistente`, `campo_somente_leitura`, `referencia_invalida`). Propriedade ausente no objeto é removida do Pset. Medição: `python .cursor/skills/ifc-python/medir_objetos.py N` (Postgres local). Relatório: `projects/plataforma-projetos/docs/poc/objetos-ifc.md`.

## Regras para agentes
1. Sempre abra com `ifcopenshell.open()` e confira `f.schema` antes de editar; não converta esquema silenciosamente.
2. Edite pelo `ifcopenshell.api.*` (mantém relações e histórico de dono coerentes), não criando entidades cruas, salvo leitura.
3. Script da IA nunca grava por cima: cada execução gera **novo arquivo** (versão/commit) e roda `validar_ids` + `ifcopenshell.validate` antes de aceitar.
4. Preserve `GlobalId` dos elementos existentes; é a identidade do histórico e do diff.
5. Rode scripts gerados pela IA em processo isolado com tempo e memória limitados (o modelo pode ter milhares de elementos).
6. `ids.open(caminho)` não valida o XML contra o XSD por padrão; use `validate=True` ao receber IDS de terceiros.

## Checklist
- [ ] `f.schema` conferido e registrado na versão.
- [ ] Unidades conferidas: API em metro; entidade crua e leitura de geometria na unidade do arquivo (`ifcopenshell.util.unit.calculate_unit_scale`).
- [ ] IDS do projeto aprovado; falhas devolvidas ao usuário em texto.
- [ ] Teste unitário para cada receita nova.

## Fontes
- Docs IfcOpenShell 0.9 (API): https://docs.ifcopenshell.org/autoapi/ifcopenshell/api/index.html
- ifctester: https://docs.ifcopenshell.org/ifctester.html
- Licença LGPL-3.0 do IfcOpenShell: https://github.com/IfcOpenShell/IfcOpenShell/blob/v0.8.0/COPYING.LESSER
- Exemplo tek usado como referência (não copiado): `tekto-model/exemplos/ifcopenshell/parede_generica.py` (TM-258); IDS por categoria: `tek-catalog/ids/` (TK-007).
