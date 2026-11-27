import { afterEach, describe, expect, it, vi } from "vitest";
import { saidaAssistente } from "@/src/agentes/contrato";
import { modeloFalsoSomar } from "@/src/agentes/harness/modelo-falso";
import { criarPost } from "@/src/agentes/rotas/agente";
import { executarExemplo } from "@/src/agentes/servicos/exemplo";
import { definicaoSomar } from "@/src/agentes/tools/exemplo";

function pedido(corpo: string, agente = "exemplo") {
  return {
    req: new Request(`http://localhost/api/agentes/${agente}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: corpo,
    }),
    ctx: { params: Promise.resolve({ agente }) },
  };
}

describe("POST /api/agentes/[agente]", () => {
  const anterior = process.env.AGENT_MODELO_FALSO;

  afterEach(() => {
    if (anterior === undefined) {
      delete process.env.AGENT_MODELO_FALSO;
    } else {
      process.env.AGENT_MODELO_FALSO = anterior;
    }
    vi.unstubAllEnvs();
  });

  it("entrada válida devolve 200 com schema, trace_id e tool", async () => {
    process.env.AGENT_MODELO_FALSO = "1";
    const POST = criarPost();
    const { req, ctx } = pedido(JSON.stringify({ objetivo: "Some 1 e 2" }));
    const res = await POST(req, ctx);
    expect(res.status).toBe(200);
    const corpo = saidaAssistente.parse(await res.json());
    expect(corpo.dados).toEqual({ total: 3 });
    expect(corpo.toolsChamadas).toContain("somar");
    expect(corpo.trace_id).toEqual(expect.any(String));
    expect(corpo.passos).toBeGreaterThanOrEqual(2);
  });

  it("entrada inválida devolve 422 no formato RFC 9457", async () => {
    const POST = criarPost();
    const { req, ctx } = pedido(JSON.stringify({ objetivo: "" }));
    const res = await POST(req, ctx);
    expect(res.status).toBe(422);
    const corpo = await res.json();
    expect(corpo).toMatchObject({
      type: "about:blank",
      title: "Entrada inválida",
      status: 422,
    });
    expect(typeof corpo.detail).toBe("string");
    expect(corpo.detail.length).toBeGreaterThan(0);
    expect(corpo.detail.startsWith("[")).toBe(false);
  });

  it("erro de tool devolve corpo estruturado, genérico e nunca stack trace", async () => {
    process.env.AGENT_MODELO_FALSO = "1";
    const falha = new Error("falha na tool");
    falha.stack = "Error: falha na tool\n    at foo.ts:1:1\n    at bar.ts:2:2";
    const POST = criarPost({
      executar: (p) =>
        executarExemplo({
          ...p,
          modelo: modeloFalsoSomar(),
          tools: [
            {
              ...definicaoSomar,
              executar: () => {
                throw falha;
              },
            },
          ],
        }),
    });
    const { req, ctx } = pedido(JSON.stringify({ objetivo: "Some 1 e 2" }));
    const res = await POST(req, ctx);
    expect(res.status).toBe(500);
    const corpo = await res.json();
    const bruto = JSON.stringify(corpo);
    expect(corpo).toMatchObject({
      type: "about:blank",
      title: "Falha no agente",
      status: 500,
      codigo: "ERRO_INTERNO",
    });
    expect(typeof corpo.trace_id).toBe("string");
    expect(corpo.detail).toBe(
      `Falha interna. Informe o trace_id ${corpo.trace_id} se precisar de suporte.`,
    );
    expect(corpo).not.toHaveProperty("stack");
    expect(bruto).not.toContain("falha na tool");
    expect(bruto).not.toContain("foo.ts");
    expect(bruto).not.toContain("bar.ts");
    expect(bruto).not.toContain("at foo");
    expect(bruto).not.toMatch(/\n\s*at /);
  });

  it("recusa AGENT_MODELO_FALSO em produção e ainda devolve trace_id", async () => {
    process.env.AGENT_MODELO_FALSO = "1";
    vi.stubEnv("NODE_ENV", "production");
    const POST = criarPost();
    const { req, ctx } = pedido(JSON.stringify({ objetivo: "Some 1 e 2" }));
    const res = await POST(req, ctx);
    expect(res.status).toBe(500);
    const corpo = await res.json();
    expect(corpo.codigo).toBe("ERRO_INTERNO");
    expect(typeof corpo.trace_id).toBe("string");
    expect(corpo.detail).not.toContain("AGENT_MODELO_FALSO");
    expect(corpo.detail).toContain(corpo.trace_id);
  });
});
