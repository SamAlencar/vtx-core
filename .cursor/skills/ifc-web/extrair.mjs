// Extração de dados IFC com web-ifc (MPL-2.0). Mesma API no navegador e no Node.
import * as WEBIFC from "web-ifc";

/** Inicia o web-ifc. `wasmPath` = pasta servida pelo próprio app (sem CDN). */
export async function iniciar(wasmPath) {
  const api = new WEBIFC.IfcAPI();
  if (wasmPath) api.SetWasmPath(wasmPath, true);
  try {
    await api.Init();
  } catch (e) {
    throw new Error(`WASM do web-ifc não carregou de "${wasmPath ?? "padrão"}": ${e.message}`);
  }
  return api;
}

/** Abre bytes de um .ifc. Devolve { modelID, schema }. */
export function abrirModelo(api, bytes) {
  const modelID = api.OpenModel(new Uint8Array(bytes), { COORDINATE_TO_ORIGIN: true });
  if (modelID < 0) throw new Error("arquivo IFC inválido");
  return { modelID, schema: api.GetModelSchema(modelID) };
}

const valor = (v) => (v && typeof v === "object" && "value" in v ? v.value : v);

/** Lista elementos de um tipo (ex.: "IFCWALL") com expressID, GlobalId e Name. */
export function listarElementos(api, modelID, tipo) {
  const codigo = WEBIFC[tipo.toUpperCase()];
  if (typeof codigo !== "number") throw new Error(`tipo IFC desconhecido: ${tipo}`);
  const ids = api.GetLineIDsWithType(modelID, codigo, true);
  const out = [];
  for (let i = 0; i < ids.size(); i++) {
    const l = api.GetLine(modelID, ids.get(i));
    out.push({ expressID: l.expressID, GlobalId: valor(l.GlobalId), Name: valor(l.Name) });
  }
  return out;
}

/** Psets do elemento (inclui os herdados do tipo): { NomePset: { prop: valor } }. */
export async function propriedades(api, modelID, expressID) {
  // 4º argumento true devolve SÓ os Psets do tipo; por isso duas chamadas (tipo primeiro, instância sobrescreve).
  const doTipo = await api.properties.getPropertySets(modelID, expressID, true, true);
  const daInstancia = await api.properties.getPropertySets(modelID, expressID, true, false);
  const out = {};
  for (const ps of [...doTipo, ...daInstancia]) {
    if (!ps.HasProperties) continue;
    const props = {};
    for (const p of ps.HasProperties) props[valor(p.Name)] = valor(p.NominalValue);
    out[valor(ps.Name)] = props;
  }
  return out;
}
