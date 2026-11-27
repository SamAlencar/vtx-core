#!/usr/bin/env node
/**
 * Extrai o primeiro bloco ```ts / ```tsx / ```typescript de cada regra VTX-210
 * para tests/regras/<nome>.exemplo.ts.
 */
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const raiz = dirname(dirname(fileURLToPath(import.meta.url)));
const dirRegras = join(raiz, ".cursor/rules");
const destino = join(raiz, "tests/regras");
const cercas = /^```(?:ts|tsx|typescript)\s*\n([\s\S]*?)```/m;
const nomes = ["stack.mdc", "api.mdc", "agentes.mdc"];

mkdirSync(destino, { recursive: true });
for (const nome of nomes) {
  const texto = readFileSync(join(dirRegras, nome), "utf8");
  const m = texto.match(cercas);
  if (!m) {
    throw new Error(`nenhum bloco ts em ${nome}`);
  }
  const base = nome.replace(/\.mdc$/, "");
  writeFileSync(join(destino, `${base}.exemplo.ts`), m[1].trimEnd() + "\n", "utf8");
}
const esperados = new Set(nomes.map((r) => r.replace(/\.mdc$/, ".exemplo.ts")));
const extra = readdirSync(destino).filter((n) => n.endsWith(".exemplo.ts") && !esperados.has(n));
if (extra.length) {
  console.warn("arquivos extra em tests/regras/:", extra.join(", "));
}
console.log("exemplos extraídos em", destino);
