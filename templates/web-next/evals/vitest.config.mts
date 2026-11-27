import path from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vitest/config";

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

export default defineConfig({
  root: raiz,
  resolve: {
    alias: { "@": raiz },
  },
  test: {
    environment: "node",
    include: ["evals/rodar.eval.ts"],
  },
});
