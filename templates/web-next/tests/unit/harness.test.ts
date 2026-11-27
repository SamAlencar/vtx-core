import { APICallError } from "ai";
import { MockLanguageModelV4 } from "ai/test";
import { describe, expect, it } from "vitest";
import { z } from "zod";
import { ErroAgente, executarAgente, type ToolDefinicao } from "@/src/agentes/harness";

const uso = {
  inputTokens: {
    total: 1,
    noCache: 1,
    cacheRead: undefined,
    cacheWrite: undefined,
  },
  outputTokens: { total: 1, text: 1, reasoning: undefined },
};

const somar: ToolDefinicao<{ a: number; b: number }, number> = {
  nome: "somar",
  descricao: "Soma dois números.",
  entrada: z.object({ a: z.number(), b: z.number() }),
  saida: z.number(),
  executar: ({ a, b }) => a + b,
};

const saidaFinal = z.object({ total: z.number() });

function modeloTexto(texto: string) {
  return new MockLanguageModelV4({
    doGenerate: async () => ({
      content: [{ type: "text", text: texto }],
      finishReason: { unified: "stop", raw: undefined },
      usage: uso,
      warnings: [],
    }),
  });
}

function modeloSequencia(
  respostas: Array<
    | { tipo: "texto"; texto: string }
    | { tipo: "tool"; nome: string; input: unknown }
    | { tipo: "erro"; erro: unknown }
    | { tipo: "atraso"; ms: number; texto: string }
  >,
) {
  let i = 0;
  return new MockLanguageModelV4({
    doGenerate: async ({ abortSignal }) => {
      const atual = respostas[Math.min(i, respostas.length - 1)];
      i += 1;
      if (atual.tipo === "erro") {
        throw atual.erro;
      }
      if (atual.tipo === "atraso") {
        await new Promise<void>((resolve, reject) => {
          const t = setTimeout(resolve, atual.ms);
          abortSignal?.addEventListener("abort", () => {
            clearTimeout(t);
            reject(abortSignal.reason ?? new Error("aborted"));
          });
        });
        return {
          content: [{ type: "text", text: atual.texto }],
          finishReason: { unified: "stop" as const, raw: undefined },
          usage: uso,
          warnings: [],
        };
      }
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

function erroTransitorio() {
  return new APICallError({
    message: "serviço indisponível",
    url: "http://exemplo.local/modelo",
    requestBodyValues: {},
    statusCode: 503,
    isRetryable: true,
  });
}

describe("executarAgente", () => {
  it("para em maxIteracoes", async () => {
    const modelo = modeloSequencia([
      { tipo: "tool", nome: "somar", input: { a: 1, b: 2 } },
    ]);
    await expect(
      executarAgente({
        objetivo: "some sempre",
        tools: [somar],
        modelo,
        maxIteracoes: 2,
        timeoutMs: 2000,
        esperar: async () => undefined,
      }),
    ).rejects.toMatchObject({ codigo: "MAX_ITERACOES" } satisfies Partial<ErroAgente>);
  });

  it("aborta em timeoutMs com erro tipado", async () => {
    const modelo = modeloSequencia([{ tipo: "atraso", ms: 400, texto: "{}" }]);
    await expect(
      executarAgente({
        objetivo: "demore",
        tools: [somar],
        modelo,
        maxIteracoes: 3,
        timeoutMs: 40,
      }),
    ).rejects.toMatchObject({ codigo: "TIMEOUT" } satisfies Partial<ErroAgente>);
  });

  it("tool desconhecida vira FUNCAO_DESCONHECIDA", async () => {
    const modelo = modeloSequencia([{ tipo: "tool", nome: "xyz", input: {} }]);
    await expect(
      executarAgente({
        objetivo: "chame xyz",
        tools: [somar],
        modelo,
        maxIteracoes: 2,
        timeoutMs: 2000,
      }),
    ).rejects.toMatchObject({ codigo: "FUNCAO_DESCONHECIDA" } satisfies Partial<ErroAgente>);
  });

  it("argumento inválido vira PARAMETRO_INVALIDO com campo", async () => {
    const modelo = modeloSequencia([
      { tipo: "tool", nome: "somar", input: { a: "x" } },
    ]);
    try {
      await executarAgente({
        objetivo: "some errado",
        tools: [somar],
        modelo,
        maxIteracoes: 2,
        timeoutMs: 2000,
      });
      throw new Error("deveria ter falhado");
    } catch (erro) {
      expect(erro).toBeInstanceOf(ErroAgente);
      const e = erro as ErroAgente;
      expect(e.codigo).toBe("PARAMETRO_INVALIDO");
      expect(e.campo).toBe("a");
    }
  });

  it("falha do modelo principal usa o fallback", async () => {
    const principal = modeloSequencia([{ tipo: "erro", erro: erroTransitorio() }]);
    const fallback = modeloTexto('{"total":3}');
    const r = await executarAgente({
      objetivo: "some 1 e 2",
      tools: [somar],
      modelo: principal,
      fallback,
      maxIteracoes: 2,
      timeoutMs: 2000,
      esperar: async () => undefined,
      saida: saidaFinal,
    });
    expect(r.dados).toEqual({ total: 3 });
    expect(r.texto).toBe('{"total":3}');
    expect(r.trace_id).toEqual(expect.any(String));
  });

  it("saída final valida no schema Zod e registra a tool", async () => {
    const modelo = modeloSequencia([
      { tipo: "tool", nome: "somar", input: { a: 1, b: 2 } },
      { tipo: "texto", texto: '{"total":3}' },
    ]);
    const r = await executarAgente({
      objetivo: "some 1 e 2",
      tools: [somar],
      modelo,
      maxIteracoes: 4,
      timeoutMs: 2000,
      saida: saidaFinal,
    });
    expect(r.dados).toEqual({ total: 3 });
    expect(r.toolsChamadas).toEqual(["somar"]);
    expect(r.passos).toBe(2);
  });

  it("saída que não passa no schema vira ERRO_INTERNO", async () => {
    const modelo = modeloTexto("nao-e-json");
    await expect(
      executarAgente({
        objetivo: "fale",
        tools: [somar],
        modelo,
        maxIteracoes: 1,
        timeoutMs: 2000,
        saida: saidaFinal,
      }),
    ).rejects.toMatchObject({ codigo: "ERRO_INTERNO" } satisfies Partial<ErroAgente>);
  });

  it("timeout também cobre tool que não resolve", async () => {
    const travada: typeof somar = {
      ...somar,
      executar: () => new Promise(() => undefined),
    };
    const modelo = modeloSequencia([{ tipo: "tool", nome: "somar", input: { a: 1, b: 2 } }]);
    const inicio = Date.now();
    await expect(
      executarAgente({
        objetivo: "some e trave",
        tools: [travada],
        modelo,
        maxIteracoes: 3,
        timeoutMs: 80,
      }),
    ).rejects.toMatchObject({ codigo: "TIMEOUT" } satisfies Partial<ErroAgente>);
    expect(Date.now() - inicio).toBeLessThan(1500);
  });

  it("fallback também vale para erro não transitório do principal (401)", async () => {
    const principal = modeloSequencia([
      {
        tipo: "erro",
        erro: new APICallError({
          message: "unauthorized",
          url: "http://exemplo.local/modelo",
          requestBodyValues: {},
          statusCode: 401,
          isRetryable: false,
        }),
      },
    ]);
    const fallback = modeloTexto('{"total":3}');
    const r = await executarAgente({
      objetivo: "some 1 e 2",
      tools: [somar],
      modelo: principal,
      fallback,
      maxIteracoes: 2,
      timeoutMs: 2000,
      esperar: async () => undefined,
      saida: saidaFinal,
    });
    expect(r.dados).toEqual({ total: 3 });
  });

  it("envia o prompt como system e o objetivo como user", async () => {
    let visto: unknown;
    const modelo = new MockLanguageModelV4({
      doGenerate: async (opts) => {
        visto = opts;
        return {
          content: [{ type: "text", text: '{"total":3}' }],
          finishReason: { unified: "stop" as const, raw: undefined },
          usage: uso,
          warnings: [],
        };
      },
    });
    await executarAgente({
      sistema: "Prompt de sistema.",
      objetivo: "Some 1 e 2",
      tools: [somar],
      modelo,
      maxIteracoes: 1,
      timeoutMs: 2000,
      saida: saidaFinal,
    });
    const bruto = JSON.stringify(visto);
    expect(bruto).toContain("Prompt de sistema.");
    expect(bruto).toContain("Some 1 e 2");
    const papeis: string[] = [];
    const textos: string[] = [];
    const andar = (valor: unknown) => {
      if (!valor || typeof valor !== "object") {
        return;
      }
      const rec = valor as Record<string, unknown>;
      if (typeof rec.role === "string") {
        papeis.push(rec.role);
      }
      if (typeof rec.content === "string") {
        textos.push(rec.content);
      }
      if (typeof rec.text === "string") {
        textos.push(rec.text);
      }
      for (const item of Object.values(rec)) {
        if (Array.isArray(item)) {
          item.forEach(andar);
        } else if (item && typeof item === "object") {
          andar(item);
        }
      }
    };
    andar(visto);
    expect(papeis).toContain("system");
    expect(papeis).toContain("user");
    expect(textos).toContain("Prompt de sistema.");
    expect(textos).toContain("Some 1 e 2");
    expect(textos.some((t) => t.includes("Prompt de sistema.") && t.includes("Some 1 e 2"))).toBe(
      false,
    );
  });
});
