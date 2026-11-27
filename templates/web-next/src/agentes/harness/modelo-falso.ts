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

export type PassoGravado =
  | { tipo: "texto"; texto: string }
  | { tipo: "tool"; nome: string; input: unknown };

/** Sequência gravada, sem rede — para evals e testes. */
export function modeloGravado(passos: PassoGravado[]): ModeloAgente {
  let i = 0;
  return new MockLanguageModelV4({
    doGenerate: async () => {
      const atual = passos[Math.min(i, passos.length - 1)] ?? {
        tipo: "texto" as const,
        texto: "{}",
      };
      i += 1;
      if (atual.tipo === "texto") {
        return {
          content: [{ type: "text", text: atual.texto }],
          finishReason: { unified: "stop" as const, raw: undefined },
          usage: uso,
          warnings: [],
        };
      }
      return {
        content: [
          {
            type: "tool-call",
            toolCallId: `c${i}`,
            toolName: atual.nome,
            input: JSON.stringify(atual.input),
          },
        ],
        finishReason: { unified: "tool-calls" as const, raw: undefined },
        usage: uso,
        warnings: [],
      };
    },
  });
}
