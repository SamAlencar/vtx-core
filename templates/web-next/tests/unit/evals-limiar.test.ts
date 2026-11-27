import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { describe, expect, it } from "vitest";
import { avaliar } from "../../evals/avaliar";
import { rodarEvals } from "../../evals/rodar";

const limiaresOk = {
  acerto_tool: 1,
  validade_schema: 1,
  recusa_correta: 1,
  passos_medio_max: 2,
};

describe("evals", () => {
  it("avalia abaixo do limiar quando a barra fica acima do resultado", () => {
    const falhas = avaliar(
      { acerto_tool: 1, validade_schema: 1, recusa_correta: 1, passos_medio: 2 },
      { ...limiaresOk, acerto_tool: 1.1 },
    );
    expect(falhas).toEqual([
      { metrica: "acerto_tool", obtido: 1, limiar: 1.1 },
    ]);
  });

  it("falha quando o número médio de passos excede o limiar", async () => {
    const falhas = avaliar(
      { acerto_tool: 1, validade_schema: 1, recusa_correta: 1, passos_medio: 2.5 },
      limiaresOk,
    );
    expect(falhas).toEqual([
      { metrica: "passos_medio_max", obtido: 2.5, limiar: 2 },
    ]);

    const dir = await mkdtemp(path.join(tmpdir(), "evals-passos-"));
    const saida = path.join(dir, "resultado.json");
    const { relatorio } = await rodarEvals({
      limiares: path.resolve("evals/fixtures/limiares-passos.json"),
      saida,
    });
    expect(relatorio.ok).toBe(false);
    expect(relatorio.falhas.some((f) => f.metrica === "passos_medio_max")).toBe(true);
    expect(relatorio.metricas.passos_medio).toBeGreaterThan(1);
  });

  it("npm run evals sai com código diferente de 0 se o limiar está acima do resultado", async () => {
    const dir = await mkdtemp(path.join(tmpdir(), "evals-"));
    const saida = path.join(dir, "resultado.json");
    const { relatorio } = await rodarEvals({
      limiares: path.resolve("evals/fixtures/limiares-inatingiveis.json"),
      saida,
    });
    expect(relatorio.ok).toBe(false);
    expect(relatorio.falhas.some((f) => f.metrica === "acerto_tool")).toBe(true);
    const gravado = JSON.parse(await readFile(saida, "utf8")) as { ok: boolean };
    expect(gravado.ok).toBe(false);

    const proc = spawnSync(
      "npm",
      ["run", "evals"],
      {
        cwd: path.resolve("."),
        env: { ...process.env, EVALS_LIMIARES: path.resolve("evals/fixtures/limiares-inatingiveis.json") },
        encoding: "utf8",
      },
    );
    expect(proc.status, proc.stderr + proc.stdout).not.toBe(0);
  });
});
