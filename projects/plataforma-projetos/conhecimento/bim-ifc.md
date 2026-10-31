# Domínio BIM/IFC — base para a plataforma-projetos

> VTX-143 · 31/10/2026 · fontes abertas (buildingSMART no GitHub, docs IfcOpenShell e That Open). Nomes de entidades conferidos com IfcOpenShell 0.9.0 nos esquemas IFC2X3, IFC4 e IFC4X3_ADD2. Sem texto de ABNT nem fonte paga.

## 1. Para que serve
O núcleo da plataforma ("GitHub de projetos") é o arquivo IFC: a IA gera scripts IfcOpenShell que produzem uma nova versão, o navegador mostra o modelo (That Open/web-ifc) e o diff compara versões pelo GlobalId. Este doc dá o vocabulário e o mapa mínimo para VTX-144 (navegador), VTX-145 (backend), VTX-151/152 (versionamento e diff) e VTX-157 (comentários BCF).

## 2. Versões do esquema
| Esquema (`FILE_SCHEMA`) | Norma | Entidades* | Uso na plataforma |
|---|---|---|---|
| `IFC2X3` (TC1) | — (legado) | 653 | Ainda exportado por muitos softwares; **só leitura** e conversão. |
| `IFC4` (ADD2 TC1) | ISO 16739-1:2018 (retirada) | 776 | Comum em edificações; ler e visualizar. |
| `IFC4X3_ADD2` | ISO 16739-1:2024 | 876 | **Entregável padrão** (igual ao tekto-model, D-052); inclui infraestrutura (pontes, estradas, ferrovia, portos). |

\*Contagem do IfcOpenShell 0.9.0 (`schema_by_name(...).entities()`). Regra: detectar o esquema no cabeçalho e nunca assumir IFC4X3; entidades como `IfcFacility`, `IfcRoad`, `IfcBridge`, `IfcAlignment`, `IfcEarthworksCut` e `IfcCourse` não existem no IFC4.

Formatos de arquivo: `.ifc` (texto STEP, ISO 10303-21, o padrão), `.ifcXML` e `.ifcZIP` (o `.ifc` compactado).

## 3. Como um modelo é organizado
- **Identidade:** toda `IfcRoot` tem `GlobalId` (GUID de 128 bits comprimido em 22 caracteres). É a chave do diff e do merge; exportador que regera GlobalId a cada exportação quebra o histórico (risco a medir na VTX-151).
- **Estrutura espacial** (`IfcRelAggregates`): `IfcProject` → `IfcSite` → `IfcBuilding` (ou `IfcFacility`/`IfcBridge`/`IfcRoad` no 4.3) → `IfcBuildingStorey` → `IfcSpace`.
- **Elementos no espaço:** `IfcRelContainedInSpatialStructure` (pavimento contém paredes, vigas...).
- **Tipos:** `IfcWallType` etc. via `IfcRelDefinesByType`; `PredefinedType` classifica (ex.: `SHEAR`), e `USERDEFINED` + `ObjectType` quando não há valor da lista.
- **Propriedades e quantidades:** `IfcPropertySet` (ex.: `Pset_WallCommon`) e `IfcElementQuantity` (ex.: `Qto_WallBaseQuantities`) via `IfcRelDefinesByProperties`. Quantitativos (VTX-159) saem daqui.
- **Materiais e aberturas:** `IfcMaterial`/`IfcMaterialLayerSet` via `IfcRelAssociatesMaterial`; vãos por `IfcOpeningElement` com `IfcRelVoidsElement` e `IfcRelFillsElement` (porta/janela).
- **Classificação:** `IfcClassificationReference` liga a sistemas externos (ex.: bSDD, tabelas nacionais).

## 4. Mapa de entidades por disciplina
| Disciplina | Entidades principais (IFC4 e IFC4X3) | Só IFC4X3 |
|---|---|---|
| Arquitetura | `IfcWall`, `IfcSlab`, `IfcRoof`, `IfcDoor`, `IfcWindow`, `IfcStair`, `IfcRamp`, `IfcCovering`, `IfcCurtainWall`, `IfcRailing`, `IfcSpace` | — |
| Estrutura | `IfcBeam`, `IfcColumn`, `IfcSlab`, `IfcFooting`, `IfcPile`, `IfcMember`, `IfcPlate`, `IfcReinforcingBar`; análise: `IfcStructuralAnalysisModel`, `IfcStructuralCurveMember`, `IfcStructuralPointConnection` | — |
| Hidrossanitário e incêndio | `IfcPipeSegment`, `IfcPipeFitting`, `IfcValve`, `IfcSanitaryTerminal`, `IfcFireSuppressionTerminal`, `IfcDistributionSystem` | — |
| Elétrica e SPDA | `IfcCableSegment`, `IfcCableCarrierSegment`, `IfcLightFixture`, `IfcOutlet`, `IfcSwitchingDevice`, `IfcElectricDistributionBoard`, `IfcAlarm` | — |
| Climatização | `IfcDuctSegment`, `IfcAirTerminal` | — |
| Infra e terraplenagem | — | `IfcAlignment`, `IfcEarthworksCut`, `IfcEarthworksFill`, `IfcPavement`, `IfcCourse`, `IfcKerb` |
| Gestão | `IfcGroup`, `IfcZone`, `IfcTask`, `IfcCostItem`, `IfcGrid`, `IfcAnnotation` | — |

No IFC2X3 as instalações usam entidades genéricas (`IfcFlowSegment`, `IfcFlowTerminal` com tipo); por isso a importação converte ou mostra como genérico.

## 5. IDS, BCF, MVD e bSDD
- **IDS 1.0** (buildingSMART, v1.0.0 em jun/2024): XML que diz *o que* o modelo precisa ter. Facetas: entity, attribute, property, classification, material e partOf, com restrições (enumeração, padrão, faixa). Valida requisitos, **não** geometria nem esquema. Ferramenta aberta: `ifctester` (IfcOpenShell, LGPL-3.0). Reaproveitar as regras do tek-catalog (`ids/*.ids`, `tools/ids_base.py`).
- **BCF 3.0** (BCF-XML e BCF-API): tópico + comentários + *viewpoint* (câmera, recorte e componentes por `IfcGuid`). Base da VTX-157; no MVP basta guardar tópico, viewpoint e GlobalIds, com exportação `.bcfzip` depois.
- **MVD** (Model View Definition): subconjunto do esquema para um uso, ex.: *Reference View* (coordenação e visualização) e *Design Transfer View* (IFC4). O navegador mira a Reference View.
- **bSDD** (buildingSMART Data Dictionary): dicionário aberto de classes e propriedades para `IfcClassificationReference` e IDS.

## 6. Glossário
| Termo | Significado |
|---|---|
| BIM | Modelagem da informação da construção: modelo 3D com dados (não só desenho). |
| openBIM | Troca por padrões abertos da buildingSMART (IFC, IDS, BCF, bSDD), sem prender a um software. |
| IFC | Industry Foundation Classes: esquema de dados aberto (ISO 16739-1). |
| GlobalId / IfcGuid | Identificador único e estável de um objeto IFC (22 caracteres). |
| Entidade / instância | Classe do esquema (`IfcWall`) / objeto concreto no arquivo (`#123=IFCWALL(...)`). |
| Pset / Qto | Conjunto de propriedades / de quantidades padronizados (`Pset_*`, `Qto_*`). |
| PredefinedType | Subtipo enumerado de uma entidade. |
| IDS | Information Delivery Specification: requisitos verificáveis por máquina. |
| BCF | BIM Collaboration Format: apontamentos ligados a pontos de vista do modelo. |
| MVD | Recorte do esquema exigido para um tipo de troca. |
| LOD / LOIN | Nível de detalhe / nível de informação necessário em cada fase. |
| Clash | Conflito geométrico entre disciplinas. |
| Federação | Sobrepor modelos de várias disciplinas sem fundi-los. |

## 7. Implicações para o piloto
1. Detectar esquema e versão no upload; armazenar o original e um IFC4X3_ADD2 só quando a conversão for confiável.
2. Diff por GlobalId + atributos/Psets (IfcDiff do IfcOpenShell como ponto de partida, VTX-151); geometria comparada à parte.
3. Cada script gerado pela IA termina com validação de esquema e IDS base antes de virar versão (VTX-145).
4. Disciplinas do convite (VTX-156) seguem o mapa da seção 4.
5. Contexto Brasil: a Estratégia BIM BR (Decreto nº 10.306/2020) torna o IFC exigência crescente em obra pública.

## 8. Tekto (consumir, não copiar)
TK-032 (empacotar `ifc_base.py`, `ids_base.py`, `validar.py` do tek-catalog) e TM-261 (exemplos IfcOpenShell do tekto-model como funções) **ainda pendentes** em 31/10. Até lá, usar como estão: tek-catalog `ids/*.ids` (13 categorias, IDS 1.0 com ifctester 0.9.0) e tekto-model `exemplos/ifcopenshell/` e `docs/PLATAFORMA.md` (ida e volta IFC4X3_ADD2 validada no CI). Faltou: pacote instalável e funções de domínio com JSON de entrada.

## 9. Checklist
- [ ] Esquema detectado no cabeçalho antes de qualquer processamento.
- [ ] Entidade usada existe no esquema do arquivo (seção 2).
- [ ] GlobalId preservado entre versões geradas pela plataforma.
- [ ] Modelo valida no esquema e no IDS base antes do commit.
- [ ] Comentários guardam GlobalIds e viewpoint (compatível com BCF 3.0).

## 10. Fontes (acesso em 31/10/2026)
- ISO 16739-1:2024 (catálogo, IFC 4.3): https://www.iso.org/standard/84123.html
- IFC 4.x, fonte da documentação oficial: https://github.com/buildingSMART/IFC4.x-development (o site ifc43-docs.standards.buildingsmart.org bloqueia acesso automatizado, HTTP 403)
- IDS 1.0 e manual das facetas: https://github.com/buildingSMART/IDS e https://github.com/buildingSMART/IDS/tree/development/Documentation
- BCF: https://github.com/buildingSMART/BCF-XML e https://github.com/buildingSMART/BCF-API
- bSDD: https://github.com/buildingSMART/bSDD
- IfcOpenShell (ifctester, IfcDiff): https://docs.ifcopenshell.org/ifctester.html e https://docs.ifcopenshell.org/ifcdiff.html
- That Open (web-ifc): https://docs.thatopen.com/ e https://github.com/ThatOpen/engine_web-ifc
- Lacunas da VTX: [../docs/lacunas-vtx.md](../docs/lacunas-vtx.md)
