#!/usr/bin/env node
/**
 * Extrai o primeiro bloco ```ts / ```tsx / ```typescript de cada regra VTX-210
 * para tests/regras/<nome>.exemplo.ts.
 * --check: não escreve; sai com código 1 se o arquivo commitado divergir.
 */
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const checar = process.argv.includes("--check");
const raiz = dirname(dirname(fileURLToPath(import.meta.url)));
const dirRegras = join(raiz, ".cursor/rules");
const destino = join(raiz, "tests/regras");
const cercas = /^```(?:ts|tsx|typescript)\s*\n([\s\S]*?)```/m;
const nomes = ["stack.mdc", "api.mdc", "agentes.mdc"];

mkdirSync(destino, { recursive: true });
const divergencias = [];
for (const nome of nomes) {
  const texto = readFileSync(join(dirRegras, nome), "utf8");
  const m = texto.match(cercas);
  if (!m) {
    throw new Error(`nenhum bloco ts em ${nome}`);
  }
  const base = nome.replace(/\.mdc$/, "");
  const alvo = join(destino, `${base}.exemplo.ts`);
  const esperado = m[1].trimEnd() + "\n";
  if (checar) {
    if (!existsSync(alvo)) {
      divergencias.push(`${base}.exemplo.ts ausente`);
      continue;
    }
    const atual = readFileSync(alvo, "utf8");
    if (atual !== esperado) {
      divergencias.push(`${base}.exemplo.ts divergente da cerca em ${nome}`);
    }
  } else {
    writeFileSync(alvo, esperado, "utf8");
  }
}
const esperados = new Set(nomes.map((r) => r.replace(/\.mdc$/, ".exemplo.ts")));
const extra = readdirSync(destino).filter((n) => n.endsWith(".exemplo.ts") && !esperados.has(n));
if (extra.length) {
  if (checar) {
    divergencias.push("arquivos extra em tests/regras/: " + extra.join(", "));
  } else {
    console.warn("arquivos extra em tests/regras/:", extra.join(", "));
  }
}
if (checar) {
  if (divergencias.length) {
    console.error("exemplos de regras desatualizados:");
    for (const d of divergencias) console.error("-", d);
    console.error("Rode: npm run regras:extrair");
    process.exit(1);
  }
  console.log("exemplos de regras sincronizados");
  process.exit(0);
}
console.log("exemplos extraídos em", destino);
