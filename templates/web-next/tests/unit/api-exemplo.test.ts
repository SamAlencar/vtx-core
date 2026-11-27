import { describe, expect, it } from "vitest";
import { POST } from "@/app/api/exemplo/route";

function pedido(corpo: string, contentType = "application/json") {
  return new Request("http://localhost/api/exemplo", {
    method: "POST",
    headers: { "content-type": contentType },
    body: corpo,
  });
}

describe("POST /api/exemplo", () => {
  it("entrada válida devolve 200 com eco", async () => {
    const res = await POST(pedido(JSON.stringify({ mensagem: "oi" })));
    expect(res.status).toBe(200);
    await expect(res.json()).resolves.toEqual({ eco: "oi" });
  });

  it("entrada inválida devolve 422 no formato RFC 9457", async () => {
    const res = await POST(pedido(JSON.stringify({ mensagem: "" })));
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

  it("JSON malformado devolve 400 no formato RFC 9457", async () => {
    const res = await POST(pedido("{"));
    expect(res.status).toBe(400);
    const corpo = await res.json();
    expect(corpo).toEqual({
      type: "about:blank",
      title: "JSON inválido",
      status: 400,
      detail: "O corpo precisa ser um JSON válido.",
    });
  });
});
