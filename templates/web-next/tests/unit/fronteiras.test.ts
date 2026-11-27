import { spawnSync } from "node:child_process";
import path from "node:path";
import { describe, expect, it } from "vitest";

const raiz = path.resolve(import.meta.dirname, "../..");

function eslint(alvo: string) {
  return spawnSync("npx", ["eslint", alvo], {
    cwd: raiz,
    encoding: "utf8",
    env: { ...process.env, npm_config_audit: "false", npm_config_fund: "false" },
  });
}

function saida(r: ReturnType<typeof eslint>): string {
  return `${r.stdout}\n${r.stderr}`;
}

describe("fronteiras de camada", () => {
  it("npx eslint tests/fronteiras/violacao.ts acusa as duas importações", () => {
    const r = eslint("tests/fronteiras/violacao.ts");
    const texto = saida(r);
    expect(r.status, texto).not.toBe(0);
    const erros = (texto.match(/no-restricted-imports/g) ?? []).length;
    expect(erros, texto).toBeGreaterThanOrEqual(2);
    expect(texto).toMatch(/@\/src\/agentes/);
    expect(texto).toMatch(/\bai\b/);
  });

  it("npx eslint tests/fronteiras/sdk-fora-harness.ts barra o SDK fora do harness", () => {
    const r = eslint("tests/fronteiras/sdk-fora-harness.ts");
    const texto = saida(r);
    expect(r.status, texto).not.toBe(0);
    expect(texto).toMatch(/no-restricted-imports/);
    expect(texto).toMatch(/src\/agentes\/harness/);
  });
});
