import { MockLanguageModelV4 } from "ai/test";
import type { ModeloAgente } from "./executar";

const uso = {
  inputTokens: {
    total: 1,
    noCache: 1,
    cacheRead: undefined,
    cacheWrite: undefined,
  },
  outputTokens: { total: 1, text: 1, reasoning: undefined },
};

/**
 * Modelo de referência para testes e e2e: chama a tool `somar` com 1 e 2
 * e devolve `{"total":3}`. Sem rede.
 */
export function modeloFalsoSomar(): ModeloAgente {
  let passo = 0;
  return new MockLanguageModelV4({
    doGenerate: async () => {
      passo += 1;
      if (passo === 1) {
        return {
          content: [
            {
              type: "tool-call",
              toolCallId: "c1",
              toolName: "somar",
              input: JSON.stringify({ a: 1, b: 2 }),
            },
          ],
          finishReason: { unified: "tool-calls" as const, raw: undefined },
          usage: uso,
          warnings: [],
        };
      }
      return {
        content: [{ type: "text", text: '{"total":3}' }],
        finishReason: { unified: "stop" as const, raw: undefined },
        usage: uso,
        warnings: [],
      };
    },
  });
}
