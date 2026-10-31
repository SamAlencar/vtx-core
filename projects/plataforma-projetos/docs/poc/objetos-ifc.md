# Prova de risco VTX-152 — parte 1: camada de objetos sobre o IFC (Postgres)

> Status: **parte 1 concluída, VTX-152 em andamento.** Medido em 31/10/2026 numa máquina de 8 vCPU / 15 GB (2 GB livres), Python 3.13, IfcOpenShell 0.9.0.post1, PostgreSQL 17.11 local. Decisão de origem: VTX-151 §7.1 ([versionamento-ifc.md](../../../../knowledge/engenharia/bim/versionamento-ifc.md)).

## 1. O que foi testado
O IFC aprovado de cada versão continua sendo a fonte da verdade (arquivo fechado com hash). A partir dele geramos **um objeto JSON por elemento**, guardado em Postgres `jsonb`, que é a camada de trabalho da IA e do visualizador. Edições feitas nessa camada voltam ao IFC base aplicando só a diferença, e o resultado é a próxima versão.

Código: [objetos.py](../../../../.cursor/skills/ifc-python/objetos.py) (`extrair`, `aplicar`), medição em [medir_objetos.py](../../../../.cursor/skills/ifc-python/medir_objetos.py), 6 testes em [test_objetos_ifc.py](../../../../tests/test_objetos_ifc.py).

Objeto: `globalid`, `classe`, `nome`, `tipo`, `psets` (da instância), `qtos`, `materiais`, `andar`, `grupos`. Editáveis: nome, psets, andar, grupos e tipo. Somente leitura (erro `campo_somente_leitura`): classe, materiais e qtos.

## 2. Critério de aceite × resultado
| Critério (notas da VTX-152) | Resultado |
|---|---|
| Ida e volta preserva GlobalId, classe e tipo | ✅ teste idempotente: `extrair(aplicar(extrair(f)))` igual ao original após gravar e reabrir |
| Psets preservados e editáveis | ✅ criar, editar e remover propriedade (remoção = `None` no `edit_pset`) |
| Material | ✅ lido (camadas, constituintes, perfis, lista; herdado do tipo); edição fica fora da camada |
| Relações: andar, tipo, grupos | ✅ mudança de andar e de grupo volta ao IFC |
| IDS / validador | ✅ `exemplo.ids` aprova após completar `IsExternal` e reprova após removê-lo; `ifcopenshell.validate` sem erros |
| Modelo do tek-model | ✅ `catalogo_parede_exemplo.ifc` (só tipo, 3 camadas) extrai materiais e Pset do tipo |
| Modelo real grande | ⏳ ainda sintético (itens TM-261/TM-264 do Eng pendentes) |

## 3. Números (modelo sintético: paredes, 10 andares, 5 tipos, 10 grupos; v2 = 1% editado + 101 edições em SQL)
| Etapa | 2.000 paredes (2,1 MB) | 20.000 paredes (22,2 MB) |
|---|---|---|
| Abrir IFC | 0,06 s | 0,82 s |
| Extrair objetos | 0,16 s | 1,67 s |
| Carga `COPY` (2 versões) + índice GIN | 44 ms | 432 ms |
| Consulta "paredes externas do Pav 2" (`@>`) | 0,7 ms | 3,3 ms |
| Contagem por andar | 0,8 ms | 7,6 ms |
| Busca por GlobalId | 0,1 ms | 0,3 ms |
| Editar 1 / 100 objetos | 0,7 / 2,1 ms | 0,7 / 2,0 ms |
| Diff v1×v2 em SQL | 3,2 ms | 26,4 ms |
| Tamanho da tabela (2 versões) | 2,9 MB | 24 MB |
| Volta ao IFC (ler todos, aplicar, gravar) | 0,31 s | 3,43 s |
| Diff IFC v1×v2 por GlobalId (conferência) | 0,28 s (120 alterados = SQL) | 3,21 s (299 = SQL) |

Leitura: consultas e edições da IA ficam na casa de milissegundos mesmo com 20 mil elementos. O gargalo é a volta ao IFC, que hoje relê todos os objetos. Mandar só os alterados (o diff SQL já os entrega) reduz isso para o custo das edições. Gerar o modelo pela API levou 186 s com 20 mil paredes; é custo do gerador sintético, não da camada.

## 4. Achado de bug
`receitas.validar_ids` abria o IFC dentro de `validate()`. O arquivo era coletado da memória antes do relatório, que então falhava com `Instance #n not found` sempre que havia elemento aprovado com tipo. Agora a referência fica viva até o fim; o teste de IDS cobre o caso.

## 5. Decisão parcial
**Índice próprio no Postgres: viável** para o MVP como camada de trabalho (consultas e edições em ms, diff em SQL igual ao diff no IFC, sem serviço extra nem custo). Ainda não comparado com o Speckle.

## 6. Falta (parte 2, mantém a VTX-152 em andamento)
- [ ] Speckle hospedado por nós (Apache-2.0): precisa de Docker, que esta máquina não tem; rodar onde houver Docker e medir as mesmas consultas e a ida e volta.
- [ ] Fluidez 3D e diff visual (destacar alterados) no navegador: That Open (skill [ifc-web](../../../../.cursor/skills/ifc-web/SKILL.md)) × visualizador do Speckle, em navegador real.
- [ ] Repetir com modelos reais do Eng (TM-261/TM-264) e com o validador do tek-catalog (TK-032).
- [ ] Volta ao IFC só com os objetos alterados; criação de elemento continua pelas funções de domínio ([funcoes-de-dominio.md](../../../../knowledge/engenharia/ia/funcoes-de-dominio.md)).

## Fontes
- IfcOpenShell `util.element` (get_psets, get_material, get_container, get_type): https://docs.ifcopenshell.org/autoapi/ifcopenshell/util/element/index.html
- `api.pset.edit_pset` (valor `None` remove a propriedade): https://docs.ifcopenshell.org/autoapi/ifcopenshell/api/pset/edit_pset/index.html
- PostgreSQL 17, índices GIN em jsonb (`jsonb_path_ops`, operador `@>`): https://www.postgresql.org/docs/17/datatype-json.html
- Speckle Server (licença): https://github.com/specklesystems/speckle-server
