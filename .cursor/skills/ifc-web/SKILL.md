---
name: ifc-web
description: Use ao abrir, navegar, selecionar ou extrair propriedades de modelos IFC no navegador (That Open Components 3.6 + Fragments + web-ifc), inclusive para destacar elementos alterados entre duas versões.
---

# IFC no navegador (That Open Components + web-ifc)

Exemplo testado: `extrair.mjs` (web-ifc, roda igual no Node e no navegador; testes `extrair.test.mjs`) e `visualizador.ts` (compila com `npm run typecheck` e `npm run build`). Backend e diff por GlobalId: skill `ifc-python`. Domínio: `projects/plataforma-projetos/conhecimento/bim-ifc.md`.

## Pacotes (pin exato, todos grátis)
| Pacote | Versão | Licença | Papel |
|---|---|---|---|
| `@thatopen/components` | 3.6.0 | MIT | Mundo 3D, câmera, `IfcLoader`, `FragmentsManager` |
| `@thatopen/fragments` | 3.6.0 | MIT | Formato Fragments + Worker (geometria fora da thread principal) |
| `web-ifc` | 0.0.78 | MPL-2.0 | Parser IFC em WASM; usar sem modificar (MPL vale só para arquivos alterados) |
| `three` / `camera-controls` | 0.187.0 / 3.1.2 | MIT | Peers exigidos pelos pacotes acima |

`npm ci && npm test && npm run typecheck && npm run build` (CI: job `ifc-web` em `testes.yml`).

## Receitas
| Tarefa | Onde | Observação |
|---|---|---|
| Abrir e saber o esquema | `abrirModelo(api, bytes)` | Devolve `schema` (IFC2X3/IFC4/IFC4X3); registre-o na versão. |
| Listar elementos | `listarElementos(api, id, "IFCWALL")` | Tipo desconhecido gera erro claro; inclui subtipos. |
| Propriedades | `propriedades(api, id, expressID)` | `{Pset: {prop: valor}}`; sem Pset devolve `{}`. |
| Ver em 3D | `criarVisualizador(div).carregar(bytes)` | Converte IFC em Fragments no Worker. |
| Destacar diff | `destacar(model, guids, cor)` | Casa por GlobalId (mesma chave da VTX-151). |
| Painel de dados | `dados(model, localId)` | Atributos + `IsDefinedBy` (Psets). |

## Regras para agentes
1. **Sem CDN em runtime:** `autoSetWasm: false` + `wasm.path` próprio e `fragments.init("/worker/worker.mjs")`. `FragmentsManager.getWorker()` e o WASM automático baixam do unpkg; não use (LGPD, disponibilidade, versão).
2. Copie `node_modules/web-ifc/web-ifc.wasm` e `node_modules/@thatopen/fragments/dist/Worker/worker.mjs` para a pasta pública no build; versão do WASM tem de bater com a do `web-ifc`.
3. `getPropertySets(..., true, true)` devolve **só** os Psets do tipo; para instância + tipo, chame com `false` e `true` e mescle (já feito em `propriedades`).
4. Arquivo grande: converta IFC em `.frag` uma vez (no backend ou no primeiro upload) e guarde; reabrir `.frag` é bem mais rápido que reconverter. Números reais ficam na VTX-152.
5. Edição de geometria não acontece no navegador: o front só mostra e seleciona; a mudança volta como script/função para o backend (`ifc-python`), que gera a nova versão.
6. Trate falha de WASM e arquivo inválido com mensagem ao usuário (as funções lançam erro com texto claro).

## Checklist
- [ ] Pins exatos e `package-lock.json` versionado.
- [ ] WASM e Worker servidos do próprio domínio (nenhuma requisição ao unpkg na aba Rede).
- [ ] Esquema do arquivo exibido/registrado.
- [ ] Teste `node --test` para cada receita nova.

## Fontes
- That Open Components (MIT): https://github.com/ThatOpen/engine_components
- Fragments (MIT): https://github.com/ThatOpen/engine_fragment
- web-ifc (MPL-2.0): https://github.com/ThatOpen/engine_web-ifc
- Tutoriais: https://docs.thatopen.com/Tutorials/Components/Core/IfcLoader
- MPL-2.0 FAQ: https://www.mozilla.org/en-US/MPL/2.0/FAQ/
