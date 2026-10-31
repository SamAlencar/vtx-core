# Versionamento de modelos IFC: versões, branches, diff e merge

> VTX-151 · 31/10/2026 · Proposta de ADR (status **proposto**, nível A1: decisão técnica reversível, não precisa do Samuel). É o diferencial "GitHub de projetos de construção" da plataforma-projetos. Base: [domínio BIM/IFC](../../../projects/plataforma-projetos/conhecimento/bim-ifc.md), [skill ifc-python](../../../.cursor/skills/ifc-python/SKILL.md) e [modelagem de dados](../../tecnologia/modelagem-de-dados.md).

## 1. Contexto
O piloto exige, no lançamento: cada alteração (humana ou da IA) vira uma versão com autor, comparável e reversível; branches; diff visual; merge. A IA edita gerando script IfcOpenShell que o backend executa, produzindo um IFC novo (commit). Precisamos decidir **identidade**, **armazenamento**, **diff** e **merge** com ferramentas grátis.

## 2. Identidade: GlobalId
- Todo `IfcRoot` tem `GlobalId` (22 caracteres, base64 de um GUID). É a chave do diff, como o IfcDiff do IfcOpenShell também assume.
- **Risco:** exportadores que regeram GlobalId a cada exportação. Medido abaixo: o diff vira "tudo removido + tudo adicionado".
- **Mitigação:** (1) commits feitos pela plataforma (IA/edição) preservam GlobalId por regra da skill; (2) no upload, se > 50% dos GlobalId mudarem e a contagem por classe for parecida, avisar o usuário e oferecer **casamento heurístico** (classe + `Tag` + nome + centro do bounding box), gravando o mapa `GlobalId antigo → novo` no commit.

## 3. Medição local (IfcOpenShell 0.9.0.post1, ifcdiff 0.9.0, 2.000 paredes, máquina da VTX)
v2 = v1 com 10 Psets alterados, 5 renomeadas, 10 removidas e 20 novas. Script: [`medir_diff.py`](../../../.cursor/skills/ifc-python/medir_diff.py), usando as funções da skill.

| Medida | Resultado |
|---|---|
| `diff_por_globalid` (classe, nome, Psets) | 20 adicionadas, 10 removidas, 15 alteradas, **0,15 s** |
| IfcDiff atributos + propriedades | mesmo resultado, **0,62 s** |
| IfcDiff geometria (1.990 elementos comparados) | 0 alteradas (correto), **1,4 s** |
| Mesmo v2 com GlobalId regerados | 2.010 adicionadas, 2.000 removidas, 0 alteradas |
| Tamanho v1 / v2 (STEP) | 2,10 MB / 2,11 MB; gzip 400 KB / 401 KB |
| Delta de texto (unified diff) v1→v2 | 56 KB; gzip **15 KB** (≈ 4% do gzip completo) |

Leitura: diff semântico é barato nesse porte; geometria custa ~10× mais e deve rodar em segundo plano. Delta de texto só fica pequeno porque o IfcOpenShell preservou os ids `#n` do STEP; ferramentas de autoria (Revit etc.) renumeram tudo, e aí o delta textual explode. A VTX-152 repete com arquivos reais grandes.

## 4. Opções de armazenamento
| Opção | Como | Prós | Contras |
|---|---|---|---|
| **A. Snapshot completo** | Cada commit = IFC inteiro (gzip) no Storage, endereçado pelo SHA-256 | Simples, abre direto no viewer, reverter = apontar; robusto a renumeração | Espaço: 400 KB por versão no exemplo; arquivo real de 50 MB × 100 versões pesa |
| B. Delta textual (estilo git) | Guarda diff de linhas STEP | Pequeno quando ids `#n` se mantêm | Quebra com renumeração; reconstruir versão antiga é lento; frágil |
| C. Objetos por hash (estilo Speckle) | Quebra o modelo em objetos JSON imutáveis com hash; commit = árvore de hashes | Dedup real entre versões, diff = comparar hashes, base para merge | Reescrever serialização IFC ↔ objetos; perde fidelidade se mal feito; esforço G |
| **D. Híbrido (proposto)** | A + índice por elemento: tabela `elemento_versao(commit, globalid, classe, nome, hash_psets, hash_geom)` | Diff instantâneo por SQL; viewer usa o snapshot; caminho para C depois | Duplica espaço em arquivos (aceitável no MVP); índice a manter |

Referências abertas: Speckle (servidor Apache-2.0 fora dos módulos EE; modelo de objetos com hash e commits) como inspiração de C; BIMserver (AGPL-3.0, guarda IFC em banco com revisões) só como referência, **não** adotar no SaaS pela AGPL; IFC5/IFCX (buildingSMART, alfa, composição em camadas JSON) acompanhar, ainda não usar.

## 5. Diff semântico (o que a plataforma mostra)
1. **Nível elemento:** adicionado / removido / alterado por GlobalId (índice da opção D).
2. **Nível propriedade:** quais Psets/atributos mudaram, valor antigo → novo (IfcDiff `attributes`, `property`, `type`, `container`).
3. **Nível geometria:** hash da geometria triangulada por elemento; se mudou, marcar "geometria alterada" e, sob demanda, IfcDiff `geometry`.
4. **Visual:** viewer pinta verde/vermelho/amarelo pelos GlobalId (VTX-144/152).

## 6. Branches e merge
- **Branch** = ponteiro nomeado para um commit (como git); commit guarda `pai` (e `pai2` no merge), autor, mensagem, origem (`humano`/`ia`/`upload`), esquema IFC e hash do arquivo.
- **Merge de 3 vias por elemento:** base = ancestral comum. Para cada GlobalId: mudou só de um lado → aplica; mudou igual nos dois → aplica; mudou diferente → **conflito**. Granularidade de conflito: propriedade (Pset.prop) ou geometria inteira.
- **Aplicação:** o merge gera um script IfcOpenShell (mesmo caminho da IA) sobre a cópia da branch destino; nunca edição manual do STEP.
- **Conflitos no MVP:** o usuário escolhe "minha / dele" por elemento; sem fusão de geometria. Relações (contenção, aberturas `IfcRelVoidsElement`) entram como atributo do elemento: remover uma parede que tem janela na outra branch é conflito obrigatório.
- **Pré-condição de merge:** mesmo esquema IFC nos dois lados; IDS do projeto aprovado no resultado.

## 7. Decisão proposta
Adotar **D (snapshot completo + índice por elemento)** no MVP, identidade por GlobalId com casamento heurístico no upload, diff em três níveis (elemento e propriedade síncronos, geometria em fila) e merge de 3 vias por elemento com conflito resolvido pelo usuário. Revisitar C (objetos por hash) se o armazenamento passar de ~5 GB por projeto ativo ou se o merge precisar de granularidade menor que o elemento.

## 7.1 Decisão de 31/10 (grupo Plataforma de Projetos)
- Cada versão aprovada pelo projetista é guardada como um **IFC fechado e imutável, com data e hash SHA-256**. Esse arquivo é o entregável e o que vale para a ART (a Estratégia BIM BR, Decreto 11.888/2024, exige entrega em formato aberto).
- A camada de objetos / índice por elemento é **gerada a partir desse IFC** e funciona como camada de trabalho do dia a dia para a IA e o visualizador. A escolha entre Speckle hospedado e índice próprio no Postgres fica para a prova de risco VTX-152. Parte 1 (índice próprio no Postgres) medida e viável: [poc/objetos-ifc.md](../../../projects/plataforma-projetos/docs/poc/objetos-ifc.md).

## 8. Consequências
- (+) Entregável no prazo de março/2027 com IfcOpenShell + IfcDiff (LGPL, por import) e Postgres; reverter e abrir versão antiga são triviais.
- (+) O índice permite diff e "quem mudou o quê" por SQL, sem abrir arquivos.
- (−) Espaço cresce linearmente; mitigar com gzip, dedup por SHA-256 e limite de armazenamento por plano (proposta; o histórico completo vale em todos os planos, inclusive Free, por decisão do Samuel).
- (−) Exportadores que regeram GlobalId degradam o diff; o casamento heurístico é aproximado e deve ser rotulado assim na tela.

## 9. Checklist de implementação
- [ ] Tabelas `commit`, `branch`, `elemento_versao` (VTX-025 como guia).
- [ ] Commit só via script IfcOpenShell que preserva GlobalId; validar IDS + `ifcopenshell.validate`.
- [ ] Detector de GlobalId regerado no upload + casamento heurístico.
- [ ] Diff de geometria em fila assíncrona com timeout.
- [ ] Merge 3 vias com teste: sem conflito, conflito de Pset, remoção × edição.
- [ ] Repetir a medição da seção 3 com arquivos reais grandes (VTX-152).

## 10. Fontes (acesso em 31/10/2026)
- IfcDiff (IfcOpenShell 0.9.0post1): https://docs.ifcopenshell.org/ifcdiff.html
- IfcOpenShell (LGPL-3.0): https://github.com/IfcOpenShell/IfcOpenShell
- Speckle server (Apache-2.0 + módulos EE): https://github.com/specklesystems/speckle-server/blob/main/LICENSE
- Esquema de dados do Speckle: https://docs.speckle.systems/developers/data-schema/overview
- BIMserver (AGPL-3.0): https://github.com/opensourceBIM/BIMserver
- IFC5 (alfa): https://github.com/buildingSMART/IFC5-development
- Tekto: itens TM-262, TM-263 e TS-090 (VTX-F13) ainda pendentes; nada consumido deles nesta tarefa.
