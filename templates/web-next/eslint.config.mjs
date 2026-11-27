import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { FlatCompat } from "@eslint/eslintrc";

const compat = new FlatCompat({
  baseDirectory: dirname(fileURLToPath(import.meta.url)),
});

const msgDominio =
  "src/dominio não importa src/agentes nem o SDK de modelo.";
const msgSdk = "SDK de modelo só em src/agentes/harness/.";

const ext = "ts,tsx,js,jsx,mjs";

const config = [
  {
    ignores: [
      ".next/**",
      "node_modules/**",
      "out/**",
      "coverage/**",
      "playwright-report/**",
      "test-results/**",
      "next-env.d.ts",
    ],
  },
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    files: [`src/dominio/**/*.{${ext}}`, "tests/fronteiras/violacao.ts"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          paths: [
            { name: "ai", message: msgDominio },
          ],
          patterns: [
            {
              group: [
                "ai/*",
                "@ai-sdk/*",
                "**/agentes",
                "**/agentes/**",
                "@/src/agentes",
                "@/src/agentes/**",
              ],
              message: msgDominio,
            },
          ],
        },
      ],
    },
  },
  {
    files: [`**/*.{${ext}}`],
    ignores: [
      "src/agentes/harness/**",
      "src/dominio/**",
      "tests/fronteiras/violacao.ts",
      "tests/unit/**",
    ],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          paths: [{ name: "ai", message: msgSdk }],
          patterns: [
            {
              group: ["ai/*", "@ai-sdk/*"],
              message: msgSdk,
            },
          ],
        },
      ],
    },
  },
];

export default config;
