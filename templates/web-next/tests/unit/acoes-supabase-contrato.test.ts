import { afterEach, describe, expect, it } from "vitest";
import type { SupabaseClient } from "@supabase/supabase-js";
import { z } from "zod";
import { executarAgente, type ToolDefinicao } from "@/src/agentes/harness";
import { modeloGravado } from "@/src/agentes/harness/modelo-falso";
import { supabaseAdmin } from "@/lib/supabase-admin";
import {
  ACAO_LEASE_MARGEM_MS,
  leaseMsDeTimeout,
  type AcaoPendente,
  type EventoAuditoria,
  type OpcoesRepositorioAcoes,
  type RepositorioAcoes,
  type StatusAcao,
} from "@/src/agentes/memoria/acoes";
import { criarRepositorioPadrao } from "@/src/agentes/memoria/acoes-padrao";
import { repositorioAcoesSupabase } from "@/src/agentes/memoria/acoes-supabase";
import { criarPostAprovar, saidaAprovar } from "@/src/agentes/rotas/aprovar";

const USUARIO_A = "11111111-1111-4111-8111-111111111111";
const USUARIO_B = "22222222-2222-4222-8222-222222222222";
const TRACE = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa";

type LinhaAcao = {
  id: string;
  usuario_id: string;
  tool: string;
  input: unknown;
  status: StatusAcao;
  trace_id: string;
  criado_em: string;
  expira_em: string;
  executando_em?: string | null;
  contexto_retomada?: unknown;
  aprovado_por?: string | null;
  aprovado_em?: string | null;
  resultado?: unknown;
  erro?: string | null;
};

type Registro = {
  acao_id: string;
  usuario_id: string;
  evento: EventoAuditoria;
  em: string;
};

type RpcChamada = { nome: string; args: Record<string, unknown> };

function intervaloParaMs(p: unknown): number {
  if (typeof p !== "string") {
    throw new Error(`p_lease inválido: ${String(p)}`);
  }
  const m = /^(\d+) seconds$/.exec(p);
  if (!m) {
    throw new Error(`p_lease inválido: ${p}`);
  }
  return Number(m[1]) * 1000;
}

/**
 * Mock do cliente que reproduz o contrato das RPCs da migração
 * `20261127000000_acoes_pendentes.sql` (auditoria inclusa nas escritas).
 */
function clienteSupabaseAcoesFalso() {
  const acoes = new Map<string, LinhaAcao>();
  const auditoria: Registro[] = [];
  const rpcs: RpcChamada[] = [];

  const ok = <T>(data: T) => ({ data, error: null });
  const fail = (message: string) => ({ data: null, error: { message } });

  function auditarRpc(
    acao_id: string,
    usuario_id: string,
    evento: EventoAuditoria,
    em: string,
  ) {
    auditoria.push({ acao_id, usuario_id, evento, em });
  }

  function rpc(nome: string, args: Record<string, unknown>) {
    rpcs.push({ nome, args });
    if (nome === "acoes_criar") {
      const id = String(args.p_id);
      const linha: LinhaAcao = {
        id,
        usuario_id: String(args.p_usuario_id),
        tool: String(args.p_tool),
        input: args.p_input,
        status: "pendente",
        trace_id: String(args.p_trace_id),
        criado_em: String(args.p_em),
        expira_em: String(args.p_expira_em),
        contexto_retomada: args.p_contexto_retomada ?? null,
      };
      acoes.set(id, linha);
      auditarRpc(id, linha.usuario_id, "criada", linha.criado_em);
      return ok(linha);
    }
    if (nome === "acoes_reivindicar") {
      const a = acoes.get(String(args.p_id));
      const em = String(args.p_em);
      const leaseMs = intervaloParaMs(args.p_lease);
      if (!a || a.usuario_id !== args.p_usuario_id) {
        return ok(null);
      }
      if (a.status === "pendente" && Date.parse(a.expira_em) <= Date.parse(em)) {
        a.status = "expirada";
        auditarRpc(a.id, String(args.p_usuario_id), "expirada", em);
        return ok(null);
      }
      if (a.status === "pendente") {
        a.status = "executando";
        a.aprovado_por = String(args.p_usuario_id);
        a.aprovado_em = em;
        a.executando_em = em;
        auditarRpc(a.id, String(args.p_usuario_id), "aprovada", em);
        return ok(a);
      }
      if (
        a.status === "executando" &&
        a.executando_em &&
        Date.parse(a.executando_em) + leaseMs <= Date.parse(em)
      ) {
        a.status = "falhou";
        a.erro = "execução interrompida (timeout da reivindicação)";
        auditarRpc(a.id, String(args.p_usuario_id), "falhou", em);
        return ok(null);
      }
      return ok(null);
    }
    if (nome === "acoes_rejeitar") {
      const a = acoes.get(String(args.p_id));
      const em = String(args.p_em);
      if (!a || a.usuario_id !== args.p_usuario_id) {
        return ok(null);
      }
      if (a.status === "pendente" && Date.parse(a.expira_em) <= Date.parse(em)) {
        a.status = "expirada";
        auditarRpc(a.id, String(args.p_usuario_id), "expirada", em);
        return ok(null);
      }
      if (a.status !== "pendente") {
        return ok(null);
      }
      a.status = "rejeitada";
      auditarRpc(a.id, String(args.p_usuario_id), "rejeitada", em);
      return ok(a);
    }
    if (nome === "acoes_concluir") {
      const a = acoes.get(String(args.p_id));
      const status = String(args.p_status);
      if (status !== "executada" && status !== "falhou") {
        return fail(`desfecho inválido: ${status}`);
      }
      if (!a || a.status !== "executando") {
        return fail(`ação ${String(args.p_id)} não está em executando`);
      }
      a.status = status;
      if (status === "executada") {
        a.resultado = args.p_resultado;
      } else {
        a.erro = args.p_erro as string | null;
      }
      const em = new Date().toISOString();
      auditarRpc(a.id, a.usuario_id, status, em);
      return ok(a);
    }
    if (nome === "acoes_auditar") {
      auditarRpc(
        String(args.p_acao_id),
        String(args.p_usuario_id),
        args.p_evento as EventoAuditoria,
        String(args.p_em),
      );
      return ok(null);
    }
    return fail(`rpc desconhecida: ${nome}`);
  }

  function from(tabela: string) {
    const filtros: Record<string, unknown> = {};
    let ordem: { col: string; asc: boolean } | undefined;
    const api = {
      select() {
        return api;
      },
      eq(col: string, val: unknown) {
        filtros[col] = val;
        return api;
      },
      order(col: string, opts?: { ascending?: boolean }) {
        ordem = { col, asc: opts?.ascending !== false };
        return api;
      },
      async maybeSingle() {
        const rows = listar();
        return ok(rows[0] ?? null);
      },
      then(
        resolve: (v: { data: unknown; error: null }) => unknown,
        reject?: (e: unknown) => unknown,
      ) {
        return Promise.resolve(ok(listar())).then(resolve, reject);
      },
    };
    function listar(): unknown[] {
      if (tabela === "acoes_pendentes") {
        return [...acoes.values()].filter((a) =>
          Object.entries(filtros).every(
            ([k, v]) => (a as Record<string, unknown>)[k] === v,
          ),
        );
      }
      if (tabela === "acoes_auditoria") {
        let rows = auditoria.filter((r) =>
          Object.entries(filtros).every(
            ([k, v]) => (r as Record<string, unknown>)[k] === v,
          ),
        );
        if (ordem) {
          const { col, asc } = ordem;
          rows = [...rows].sort((x, y) => {
            const av = String((x as Record<string, unknown>)[col] ?? "");
            const bv = String((y as Record<string, unknown>)[col] ?? "");
            return asc ? av.localeCompare(bv) : bv.localeCompare(av);
          });
        }
        return rows;
      }
      return [];
    }
    return api;
  }

  return {
    cliente: { rpc, from } as unknown as SupabaseClient,
    acoes,
    auditoria,
    rpcs,
  };
}

function acaoBase(
  id: string,
  extra: Partial<AcaoPendente> = {},
): Omit<AcaoPendente, "expira_em"> & { expira_em?: string } {
  return {
    id,
    usuario_id: USUARIO_A,
    tool: "pagar",
    input: { valor: 50 },
    status: "pendente",
    trace_id: TRACE,
    criado_em: new Date("2026-11-27T12:00:00.000Z").toISOString(),
    ...extra,
  };
}

function repoComRelogio(
  agora: { atual: Date },
  opts: OpcoesRepositorioAcoes = {},
) {
  const falso = clienteSupabaseAcoesFalso();
  const repositorio: RepositorioAcoes = repositorioAcoesSupabase(falso.cliente, {
    agora: () => agora.atual,
    ...opts,
  });
  return { ...falso, repositorio };
}

describe("supabaseAdmin", () => {
  const originalUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const originalKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  afterEach(() => {
    if (originalUrl === undefined) {
      delete process.env.NEXT_PUBLIC_SUPABASE_URL;
    } else {
      process.env.NEXT_PUBLIC_SUPABASE_URL = originalUrl;
    }
    if (originalKey === undefined) {
      delete process.env.SUPABASE_SERVICE_ROLE_KEY;
    } else {
      process.env.SUPABASE_SERVICE_ROLE_KEY = originalKey;
    }
  });

  it("devolve null sem URL ou service_role (falha segura)", () => {
    delete process.env.NEXT_PUBLIC_SUPABASE_URL;
    delete process.env.SUPABASE_SERVICE_ROLE_KEY;
    expect(supabaseAdmin()).toBeNull();
    process.env.NEXT_PUBLIC_SUPABASE_URL = "https://exemplo.supabase.co";
    expect(supabaseAdmin()).toBeNull();
  });
});

describe("criarRepositorioPadrao", () => {
  it("sem cliente cai no repositório em memória", async () => {
    const repo = criarRepositorioPadrao(null);
    const id = "33333333-3333-4333-8333-333333333333";
    await repo.criar(acaoBase(id));
    const a = await repo.buscar(id, USUARIO_A);
    expect(a).toMatchObject({ id, status: "pendente", tool: "pagar" });
    expect(await repo.buscar(id, USUARIO_B)).toBeNull();
  });

  it("com cliente usa o repositório Supabase", async () => {
    const falso = clienteSupabaseAcoesFalso();
    const repo = criarRepositorioPadrao(falso.cliente);
    const id = "44444444-4444-4444-8444-444444444444";
    await repo.criar(acaoBase(id));
    expect(falso.rpcs.map((c) => c.nome)).toEqual(["acoes_criar"]);
    expect(await repo.buscar(id, USUARIO_A)).toMatchObject({ status: "pendente" });
  });
});

describe("repositorioAcoesSupabase (contrato)", () => {
  it("cria, busca do dono (com contexto_retomada) e não vaza para outro usuário", async () => {
    const agora = { atual: new Date("2026-11-27T12:00:00.000Z") };
    const { repositorio } = repoComRelogio(agora);
    const id = "55555555-5555-4555-8555-555555555555";
    const contexto = {
      mensagens: [],
      mensagensAssistente: [],
      resultadosParciais: [],
      toolCallId: "t1",
      passo: 1,
      toolsChamadas: ["pagar"],
      maxIteracoes: 3,
    };
    await repositorio.criar({ ...acaoBase(id), contexto_retomada: contexto });
    const a = await repositorio.buscar(id, USUARIO_A);
    expect(a).toMatchObject({
      status: "pendente",
      input: { valor: 50 },
      contexto_retomada: contexto,
    });
    expect(await repositorio.buscar(id, USUARIO_B)).toBeNull();
    expect((await repositorio.auditoria(id)).map((t) => t.evento)).toEqual([
      "criada",
    ]);
  });

  it("auditar é no-op: não chama acoes_auditar nem duplica 'criada'", async () => {
    const agora = { atual: new Date("2026-11-27T12:00:00.000Z") };
    const { repositorio, rpcs } = repoComRelogio(agora);
    const id = "66666666-6666-4666-8666-666666666666";
    await repositorio.criar(acaoBase(id));
    await repositorio.auditar({
      acao_id: id,
      usuario_id: USUARIO_A,
      evento: "criada",
      em: agora.atual.toISOString(),
    });
    expect(rpcs.map((c) => c.nome)).toEqual(["acoes_criar"]);
    expect((await repositorio.auditoria(id)).map((t) => t.evento)).toEqual([
      "criada",
    ]);
  });

  it("reivindicar é atômico: o segundo recebe null", async () => {
    const agora = { atual: new Date("2026-11-27T12:00:00.000Z") };
    const { repositorio, rpcs } = repoComRelogio(agora, { timeoutMs: 5_000 });
    const id = "77777777-7777-4777-8777-777777777777";
    await repositorio.criar(acaoBase(id));
    const ganhou = await repositorio.reivindicar(
      id,
      USUARIO_A,
      agora.atual.toISOString(),
      5_000,
    );
    expect(ganhou).toMatchObject({
      status: "executando",
      aprovado_por: USUARIO_A,
    });
    const lease = rpcs.find((c) => c.nome === "acoes_reivindicar")?.args.p_lease;
    expect(lease).toBe(`${Math.ceil(leaseMsDeTimeout(5_000) / 1000)} seconds`);
    expect(lease).toBe(
      `${Math.ceil((5_000 + ACAO_LEASE_MARGEM_MS) / 1000)} seconds`,
    );
    expect(
      await repositorio.reivindicar(id, USUARIO_A, agora.atual.toISOString()),
    ).toBeNull();
    expect((await repositorio.auditoria(id)).map((t) => t.evento)).toEqual([
      "criada",
      "aprovada",
    ]);
  });

  it("rejeitar marca rejeitada e audita uma vez", async () => {
    const agora = { atual: new Date("2026-11-27T12:00:00.000Z") };
    const { repositorio } = repoComRelogio(agora);
    const id = "88888888-8888-4888-8888-888888888888";
    await repositorio.criar(acaoBase(id));
    const r = await repositorio.rejeitar(id, USUARIO_A, agora.atual.toISOString());
    expect(r).toMatchObject({ status: "rejeitada" });
    expect(
      await repositorio.rejeitar(id, USUARIO_A, agora.atual.toISOString()),
    ).toBeNull();
    expect((await repositorio.auditoria(id)).map((t) => t.evento)).toEqual([
      "criada",
      "rejeitada",
    ]);
  });

  it("TTL vencido no reivindicar marca expirada e devolve null", async () => {
    const agora = { atual: new Date("2026-11-27T12:00:00.000Z") };
    const { repositorio } = repoComRelogio(agora, { ttlMs: 1_000 });
    const id = "99999999-9999-4999-8999-999999999999";
    await repositorio.criar(acaoBase(id));
    agora.atual = new Date("2026-11-27T12:00:02.000Z");
    expect(
      await repositorio.reivindicar(id, USUARIO_A, agora.atual.toISOString()),
    ).toBeNull();
    expect(await repositorio.buscar(id, USUARIO_A)).toMatchObject({
      status: "expirada",
    });
    expect((await repositorio.auditoria(id)).map((t) => t.evento)).toContain(
      "expirada",
    );
  });

  it("lease vencido no segundo reivindicar marca falhou e devolve null", async () => {
    const agora = { atual: new Date("2026-11-27T12:00:00.000Z") };
    const { repositorio } = repoComRelogio(agora, { leaseMs: 2_000 });
    const id = "12121212-1212-4121-8121-121212121212";
    await repositorio.criar(acaoBase(id));
    expect(
      await repositorio.reivindicar(id, USUARIO_A, agora.atual.toISOString()),
    ).toMatchObject({ status: "executando" });
    agora.atual = new Date("2026-11-27T12:00:03.000Z");
    expect(
      await repositorio.reivindicar(id, USUARIO_A, agora.atual.toISOString()),
    ).toBeNull();
    expect(await repositorio.buscar(id, USUARIO_A)).toMatchObject({
      status: "falhou",
      erro: "execução interrompida (timeout da reivindicação)",
    });
  });

  it("concluir grava resultado e audita executada; fora de executando falha", async () => {
    const agora = { atual: new Date("2026-11-27T12:00:00.000Z") };
    const { repositorio } = repoComRelogio(agora);
    const id = "13131313-1313-4131-8131-131313131313";
    await repositorio.criar(acaoBase(id));
    await repositorio.reivindicar(id, USUARIO_A, agora.atual.toISOString());
    const final = await repositorio.concluir(id, {
      status: "executada",
      resultado: "pago 50",
    });
    expect(final).toMatchObject({ status: "executada", resultado: "pago 50" });
    expect((await repositorio.auditoria(id)).map((t) => t.evento)).toEqual([
      "criada",
      "aprovada",
      "executada",
    ]);
    await expect(
      repositorio.concluir(id, { status: "executada", resultado: "de novo" }),
    ).rejects.toThrow(/não está em executando/);
  });

  it("com o harness, a tool crítica só executa após aprovar e a auditoria não duplica criada", async () => {
    const falso = clienteSupabaseAcoesFalso();
    const repositorio = repositorioAcoesSupabase(falso.cliente);
    const execucoes: number[] = [];
    const pagar: ToolDefinicao<{ valor: number }, string> = {
      nome: "pagar",
      descricao: "Paga um valor (efeito irreversível).",
      entrada: z.object({ valor: z.number().positive() }),
      saida: z.string(),
      critica: true,
      executar: ({ valor }) => {
        execucoes.push(valor);
        return `pago ${valor}`;
      },
    };
    const pedido = await executarAgente({
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
    expect(pedido.status).toBe("PENDENTE_APROVACAO");
    expect(execucoes).toEqual([]);
    const POST = criarPostAprovar({
      repositorio,
      tools: [pagar],
      timeoutMs: 2000,
      autenticar: async (req) => {
        const id = req.headers.get("x-usuario-teste");
        return id ? { id } : null;
      },
    });
    const res = await POST(
      new Request(`http://localhost/api/agentes/acoes/${pedido.acao_id}/aprovar`, {
        method: "POST",
        headers: { "x-usuario-teste": USUARIO_A },
      }),
      { params: Promise.resolve({ id: pedido.acao_id! }) },
    );
    expect(res.status).toBe(200);
    expect(saidaAprovar.parse(await res.json())).toMatchObject({
      status: "executada",
      resultado: "pago 50",
    });
    expect(execucoes).toEqual([50]);
    expect(
      (await repositorio.auditoria(pedido.acao_id!)).map((t) => t.evento),
    ).toEqual(["criada", "aprovada", "executada"]);
    expect(falso.rpcs.map((c) => c.nome)).toEqual([
      "acoes_criar",
      "acoes_reivindicar",
      "acoes_concluir",
    ]);
    expect(falso.rpcs.some((c) => c.nome === "acoes_auditar")).toBe(false);
  });
});
