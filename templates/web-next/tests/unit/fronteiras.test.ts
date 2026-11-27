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

describe("fronteiras de camada", () => {
  it("npx eslint tests/fronteiras/violacao.ts sai com código diferente de 0", () => {
    const r = eslint("tests/fronteiras/violacao.ts");
    expect(r.status, r.stdout + r.stderr).not.toBe(0);
    expect(`${r.stdout}\n${r.stderr}`).toMatch(/no-restricted-imports/);
  });
});
