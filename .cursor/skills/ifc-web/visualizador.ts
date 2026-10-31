// Visualizador mínimo: That Open Components 3.6 (MIT) + Fragments + web-ifc (MPL-2.0).
// Sem CDN em runtime: sirva /wasm/web-ifc.wasm e /worker/worker.mjs do próprio app
// (copie de node_modules/web-ifc/ e node_modules/@thatopen/fragments/dist/Worker/).
import { Color } from "three";
import {
  Components, Worlds, SimpleScene, SimpleRenderer, OrthoPerspectiveCamera,
  FragmentsManager, IfcLoader,
} from "@thatopen/components";
import type { FragmentsModel } from "@thatopen/fragments";

export async function criarVisualizador(container: HTMLElement, base = "/") {
  const components = new Components();
  const world = components.get(Worlds).create<SimpleScene, OrthoPerspectiveCamera, SimpleRenderer>();
  world.scene = new SimpleScene(components);
  world.scene.setup();
  world.renderer = new SimpleRenderer(components, container);
  world.camera = new OrthoPerspectiveCamera(components);
  components.init();

  const fragments = components.get(FragmentsManager);
  fragments.init(`${base}worker/worker.mjs`); // não use FragmentsManager.getWorker(): baixa do unpkg
  world.camera.controls.addEventListener("rest", () => fragments.core.update(true));
  fragments.list.onItemSet.add(({ value: model }) => {
    model.useCamera(world.camera.three);
    world.scene.three.add(model.object);
    fragments.core.update(true);
  });

  const loader = components.get(IfcLoader);
  await loader.setup({ autoSetWasm: false, wasm: { path: `${base}wasm/`, absolute: true } });

  /** Converte o IFC em Fragments (no Worker) e mostra. Para arquivo grande, guarde o .frag convertido. */
  async function carregar(bytes: Uint8Array, nome: string): Promise<FragmentsModel> {
    const model = await loader.load(bytes, true, nome);
    await world.camera.fitToItems();
    return model;
  }

  /** Pinta elementos por GlobalId (ex.: diff da VTX-151: verde adicionado, amarelo alterado). */
  async function destacar(model: FragmentsModel, guids: string[], cor = "#f5c400") {
    const ids = (await model.getLocalIdsByGuids(guids)).filter((i): i is number => i !== null);
    await model.setColor(ids, new Color(cor));
    await fragments.core.update(true);
    return ids.length;
  }

  /** Atributos e Psets de um elemento, para o painel de propriedades. */
  async function dados(model: FragmentsModel, localId: number) {
    const [item] = await model.getItemsData([localId], { relations: { IsDefinedBy: { attributes: true, relations: true } } });
    return item;
  }

  return { components, world, carregar, destacar, dados, descartar: () => components.dispose() };
}
