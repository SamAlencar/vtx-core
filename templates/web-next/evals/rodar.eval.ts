import { expect, it } from "vitest";
import { rodarEvals } from "./rodar";

it("a suíte de evals passa nos limiares e grava resultado.json", async () => {
  const { relatorio } = await rodarEvals();
  expect(relatorio.casos).toBeGreaterThanOrEqual(20);
  expect(relatorio.ok).toBe(true);
});
