import { expect, test } from "@playwright/test";

test("o assistente completa o fluxo com o modelo falso", async ({ page }) => {
  await page.goto("/assistente");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Assistente");
  await page.getByLabel("Objetivo").fill("Some 1 e 2");
  await page.getByRole("button", { name: "Enviar" }).click();
  await expect(page.getByTestId("dados-total")).toHaveText("total: 3");
  await expect(page.getByTestId("tools-chamadas")).toContainText("somar");
  await expect(page.getByTestId("trace-id")).toContainText("trace_id:");
});
