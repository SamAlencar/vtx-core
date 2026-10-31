import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { iniciar, abrirModelo, listarElementos, propriedades } from "./extrair.mjs";

const ler = (n) => readFile(new URL(`./fixtures/${n}`, import.meta.url));

test("abre IFC4, lista paredes e lê Pset", async () => {
  const api = await iniciar();
  const m = abrirModelo(api, await ler("parede-ifc4.ifc"));
  assert.equal(m.schema, "IFC4");
  const paredes = listarElementos(api, m.modelID, "IFCWALL");
  assert.equal(paredes.length, 2);
  assert.match(paredes[0].GlobalId, /^[0-9A-Za-z_$]{22}$/);
  const ext = paredes.find((p) => p.Name === "Parede externa");
  const props = await propriedades(api, m.modelID, ext.expressID);
  assert.equal(props.Pset_WallCommon.IsExternal, true);
  api.CloseModel(m.modelID);
});

test("elemento sem Pset devolve objeto vazio", async () => {
  const api = await iniciar();
  const m = abrirModelo(api, await ler("parede-ifc4.ifc"));
  const sem = listarElementos(api, m.modelID, "IFCWALL").find((p) => p.Name === "Parede sem pset");
  assert.deepEqual(await propriedades(api, m.modelID, sem.expressID), {});
});

test("informa esquema IFC2X3", async () => {
  const api = await iniciar();
  const m = abrirModelo(api, await ler("minimo-ifc2x3.ifc"));
  assert.equal(m.schema, "IFC2X3");
  assert.equal(listarElementos(api, m.modelID, "IFCPROJECT")[0].Name, "P2x3");
});

test("caminho do WASM errado gera erro claro", async () => {
  await assert.rejects(iniciar("/caminho/inexistente/"), /WASM do web-ifc/);
});

test("tipo IFC desconhecido gera erro claro", async () => {
  const api = await iniciar();
  const m = abrirModelo(api, await ler("parede-ifc4.ifc"));
  assert.throws(() => listarElementos(api, m.modelID, "IFCPAREDE"), /tipo IFC desconhecido/);
});
