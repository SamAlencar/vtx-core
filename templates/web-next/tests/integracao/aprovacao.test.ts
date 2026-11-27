import { describe, expect, it } from "vitest";
import { z } from "zod";
import { executarAgente, type ToolDefinicao } from "@/src/agentes/harness";
import { modeloGravado } from "@/src/agentes/harness/modelo-falso";
import { repositorioAcoesEmMemoria, type OpcoesRepositorioAcoes } from "@/src/agentes/memoria/acoes";
import { criarPostAprovar, saidaAprovar } from "@/src/agentes/rotas/aprovar";
import { criarPostRejeitar } from "@/src/agentes/rotas/rejeitar";
import { aprovarAcao } from "@/src/agentes/harness";

const USUARIO_A = "11111111-1111-4111-8111-111111111111";
const USUARIO_B = "22222222-2222-4222-8222-222222222222";

function cenario(
  opts: {
    executar?: ToolDefinicao<{ valor: number }, string>["executar"];
    repo?: OpcoesRepositorioAcoes;
  } = {},
) {
  const repositorio = repositorioAcoesEmMemoria(opts.repo);
  const execucoes: number[] = [];
  const pagar: ToolDefinicao<{ valor: number }, string> = {
    nome: "pagar",
    descricao: "Paga um valor (efeito irreversível).",
    entrada: z.object({ valor: z.number().positive() }),
    saida: z.string(),
    critica: true,
    executar:
      opts.executar ??
      (({ valor }) => {
        execucoes.push(valor);
        return `pago ${valor}`;
      }),
  };
  const POST = criarPostAprovar({
    repositorio,
    tools: [pagar],
    autenticar: async (req) => {
      const id = req.headers.get("x-usuario-teste");
      return id ? { id } : null;
    },
  });
  const aprovar = (id: string, usuario: string | null = USUARIO_A) =>
    POST(
      new Request(`http://localhost/api/agentes/acoes/${id}/aprovar`, {
        method: "POST",
        headers: usuario ? { "x-usuario-teste": usuario } : {},
      }),
      { params: Promise.resolve({ id }) },
    );
  const pedirPagamento = () =>
    executarAgente({
      objetivo: "Pague 50.",
      tools: [pagar],
      modelo: modeloGravado([
        { tipo: "tool", nome: "pagar", input: { valor: 50 } },
        { tipo: "texto", texto: "ok" },
      ]),
      maxIteracoes: 3,
      timeoutMs: 2000,
      aprovacao: { repositorio, usuarioId: USUARIO_A },
    });
  const POST_REJ = criarPostRejeitar({
    repositorio,
    autenticar: async (req) => {
      const id = req.headers.get("x-usuario-teste");
      return id ? { id } : null;
    },
  });
  const rejeitar = (id: string, usuario: string | null = USUARIO_A) =>
    POST_REJ(
      new Request(`http://localhost/api/agentes/acoes/${id}/rejeitar`, {
        method: "POST",
        headers: usuario ? { "x-usuario-teste": usuario } : {},
      }),
      { params: Promise.resolve({ id }) },
    );
  return { repositorio, execucoes, aprovar, rejeitar, pedirPagamento, pagar };
}

describe("aprovação de tool crítica (VTX-213)", () => {
  it("o harness não executa a tool crítica: devolve PENDENTE_APROVACAO com acao_id", async () => {
    const { repositorio, execucoes, pedirPagamento } = cenario();
    const r = await pedirPagamento();
    expect(r.status).toBe("PENDENTE_APROVACAO");
    expect(r.acao_id).toMatch(/^[0-9a-f-]{36}$/);
    expect(execucoes).toEqual([]);
    const acao = await repositorio.buscar(r.acao_id!, USUARIO_A);
    expect(acao).toMatchObject({ status: "pendente", tool: "pagar", input: { valor: 50 } });
  });

  it("aprovar executa uma vez e grava auditoria com usuário e horário", async () => {
    const { repositorio, execucoes, aprovar, pedirPagamento } = cenario();
    const { acao_id } = await pedirPagamento();
    const res = await aprovar(acao_id!);
    expect(res.status).toBe(200);
    const corpo = saidaAprovar.parse(await res.json());
    expect(corpo).toMatchObject({ status: "executada", resultado: "pago 50", aprovado_por: USUARIO_A });
    expect(execucoes).toEqual([50]);
    const trilha = await repositorio.auditoria(acao_id!);
    expect(trilha.map((t) => t.evento)).toEqual(["criada", "aprovada", "executada"]);
    for (const t of trilha) {
      expect(t.usuario_id).toBe(USUARIO_A);
      expect(Number.isNaN(Date.parse(t.em))).toBe(false);
    }
  });

  it("segunda aprovação devolve 409 com o resultado gravado e não reexecuta", async () => {
    const { execucoes, aprovar, pedirPagamento } = cenario();
    const { acao_id } = await pedirPagamento();
    await aprovar(acao_id!);
    const res = await aprovar(acao_id!);
    expect(res.status).toBe(409);
    const corpo = await res.json();
    expect(corpo).toMatchObject({ status: 409, title: "Ação já decidida" });
    expect(corpo.acao).toMatchObject({ status: "executada", resultado: "pago 50" });
    expect(execucoes).toEqual([50]);
  });

  it("aprovações concorrentes executam uma única vez", async () => {
    const { execucoes, aprovar, pedirPagamento } = cenario();
    const { acao_id } = await pedirPagamento();
    const respostas = await Promise.all([aprovar(acao_id!), aprovar(acao_id!), aprovar(acao_id!)]);
    expect(respostas.map((r) => r.status).sort()).toEqual([200, 409, 409]);
    expect(execucoes).toEqual([50]);
  });

  it("sem usuário autenticado responde 401 e não executa", async () => {
    const { execucoes, aprovar, pedirPagamento } = cenario();
    const { acao_id } = await pedirPagamento();
    const res = await aprovar(acao_id!, null);
    expect(res.status).toBe(401);
    expect(await res.json()).toMatchObject({ type: "about:blank", status: 401 });
    expect(execucoes).toEqual([]);
  });

  it("outro usuário recebe 404 e a ação continua pendente", async () => {
    const { repositorio, execucoes, aprovar, pedirPagamento } = cenario();
    const { acao_id } = await pedirPagamento();
    const res = await aprovar(acao_id!, USUARIO_B);
    expect(res.status).toBe(404);
    expect(execucoes).toEqual([]);
    expect((await repositorio.buscar(acao_id!, USUARIO_A))?.status).toBe("pendente");
  });

  it("acao_id que não é UUID responde 422 no formato RFC 9457", async () => {
    const { aprovar } = cenario();
    const res = await aprovar("nao-e-uuid");
    expect(res.status).toBe(422);
    const corpo = await res.json();
    expect(corpo).toMatchObject({ title: "Entrada inválida", status: 422 });
    expect(corpo.detail.startsWith("[")).toBe(false);
  });

  it("tool crítica que estoura o prazo recebe o signal, fica falhou e não reexecuta", async () => {
    let chamadas = 0;
    let sinal: AbortSignal | undefined;
    const { aprovar, pedirPagamento } = cenario({
      executar: (_dados, { signal }) => {
        chamadas += 1;
        sinal = signal;
        return new Promise<string>(() => undefined);
      },
    });
    const { acao_id } = await pedirPagamento();
    const anterior = process.env.AGENT_TIMEOUT_MS;
    process.env.AGENT_TIMEOUT_MS = "40";
    try {
      const res = await aprovar(acao_id!);
      expect(res.status).toBe(200);
      expect(await res.json()).toMatchObject({ status: "falhou" });
      expect(sinal?.aborted).toBe(true);
      expect((await aprovar(acao_id!)).status).toBe(409);
      expect(chamadas).toBe(1);
    } finally {
      if (anterior === undefined) {
        delete process.env.AGENT_TIMEOUT_MS;
      } else {
        process.env.AGENT_TIMEOUT_MS = anterior;
      }
    }
  });

  it("rejeitar marca rejeitada, audita e impede a execução posterior", async () => {
    const { repositorio, execucoes, aprovar, rejeitar, pedirPagamento } = cenario();
    const { acao_id } = await pedirPagamento();
    const res = await rejeitar(acao_id!);
    expect(res.status).toBe(200);
    expect(await res.json()).toMatchObject({ status: "rejeitada" });
    expect((await repositorio.auditoria(acao_id!)).map((t) => t.evento)).toEqual(["criada", "rejeitada"]);
    const segunda = await aprovar(acao_id!);
    expect(segunda.status).toBe(409);
    expect((await segunda.json()).acao).toMatchObject({ status: "rejeitada" });
    expect(execucoes).toEqual([]);
  });

  it("ação com TTL vencido fica expirada e não executa", async () => {
    let agora = Date.parse("2026-11-27T12:00:00.000Z");
    const { execucoes, aprovar, pedirPagamento, repositorio } = cenario({
      repo: { agora: () => new Date(agora), ttlMs: 1_000 },
    });
    const { acao_id } = await pedirPagamento();
    agora += 2_000;
    const res = await aprovar(acao_id!);
    expect(res.status).toBe(409);
    expect((await res.json()).acao).toMatchObject({ status: "expirada" });
    expect(execucoes).toEqual([]);
    expect((await repositorio.auditoria(acao_id!)).map((t) => t.evento)).toContain("expirada");
  });

  it("executando com lease vencido vira falhou e não reexecuta a tool", async () => {
    let agora = Date.parse("2026-11-27T12:00:00.000Z");
    const { execucoes, aprovar, pedirPagamento, repositorio } = cenario({
      repo: { agora: () => new Date(agora), leaseMs: 50 },
    });
    const { acao_id } = await pedirPagamento();
    const ganhou = await repositorio.reivindicar(acao_id!, USUARIO_A, new Date(agora).toISOString());
    expect(ganhou?.status).toBe("executando");
    agora += 100;
    const res = await aprovar(acao_id!);
    expect(res.status).toBe(409);
    expect((await res.json()).acao).toMatchObject({
      status: "falhou",
      erro: "execução interrompida (timeout da reivindicação)",
    });
    expect(execucoes).toEqual([]);
  });

  it("depois de aprovar, o harness retoma o fluxo e devolve a resposta do modelo", async () => {
    const { repositorio, execucoes, pedirPagamento, pagar } = cenario();
    const r = await pedirPagamento();
    expect(r.status).toBe("PENDENTE_APROVACAO");
    const aprovado = await aprovarAcao({
      repositorio,
      acaoId: r.acao_id!,
      usuarioId: USUARIO_A,
      tools: [pagar],
      retomada: {
        tools: [pagar],
        // o mesmo modelo gravado do pedirPagamento já consumiu o passo da tool;
        // um modelo novo com só o texto cobre a retomada isolada.
        modelo: (await import("@/src/agentes/harness/modelo-falso")).modeloGravado([
          { tipo: "texto", texto: "pagamento concluído" },
        ]),
      },
    });
    expect(aprovado.tipo).toBe("aprovada");
    expect(execucoes).toEqual([50]);
    expect(aprovado.tipo === "aprovada" && aprovado.agente).toMatchObject({
      status: "CONCLUIDO",
      texto: "pagamento concluído",
    });
  });
});
