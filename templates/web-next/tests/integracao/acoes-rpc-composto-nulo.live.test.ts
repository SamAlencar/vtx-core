/**
 * Rodado pelo scripts/teste-rpc-acoes-composto-nulo.sh com ACOES_RPC_LIVE=1.
 * Sem essa variável (npm test no CI) a suíte é ignorada.
 */
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { acaoDaRpc, repositorioAcoesSupabase } from "@/src/agentes/memoria/acoes-supabase";
import type { SupabaseClient } from "@supabase/supabase-js";

const USUARIO_A = "11111111-1111-4111-8111-111111111111";
const USUARIO_B = "22222222-2222-4222-8222-222222222222";
const ACAO_EXEC = "66666666-6666-4666-8666-666666666666";
const TRACE = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa";

function lerJson(caminho: string | undefined): unknown {
  if (!caminho) {
    throw new Error("arquivo de json composto nulo não informado");
  }
  return JSON.parse(readFileSync(caminho, "utf8"));
}

function jsonDaSaida(stdout: string): string {
  const texto = stdout.trim();
  const inicio = texto.search(/[{\[]/);
  if (inicio >= 0) {
    for (let fim = texto.length; fim > inicio; fim -= 1) {
      const fatia = texto.slice(inicio, fim).trim();
      try {
        JSON.parse(fatia);
        return fatia;
      } catch {
        // continua encolhendo até achar um JSON completo
      }
    }
  }
  if (/\bnull\b/.test(texto)) {
    return "null";
  }
  return texto;
}

function psql(sql: string): { ok: boolean; stdout: string; stderr: string } {
  const bin = process.env.PSQL ?? "psql";
  const r = spawnSync(
    bin,
    [
      "-h",
      process.env.PGHOST ?? "127.0.0.1",
      "-p",
      process.env.PGPORT ?? "55433",
      "-U",
      process.env.PGUSER ?? "postgres",
      "-d",
      process.env.PGDATABASE ?? "postgres",
      "-v",
      "ON_ERROR_STOP=1",
      "--no-psqlrc",
      "-tA",
      "-c",
      sql,
    ],
    { encoding: "utf8" },
  );
  return {
    ok: r.status === 0,
    stdout: jsonDaSaida(r.stdout ?? ""),
    stderr: (r.stderr ?? "").trim(),
  };
}

function sqlValor(v: unknown): string {
  if (v == null) {
    return "null";
  }
  if (typeof v === "number") {
    return String(v);
  }
  if (typeof v === "string") {
    if (/^\d+ seconds$/.test(v)) {
      return `interval '${v.replace(/'/g, "''")}'`;
    }
    return `'${v.replace(/'/g, "''")}'`;
  }
  return `'${JSON.stringify(v).replace(/'/g, "''")}'::jsonb`;
}

function clienteViaPsql(): SupabaseClient {
  return {
    async rpc(nome: string, args: Record<string, unknown>) {
      const partes = Object.entries(args).map(([k, v]) => `${k} := ${sqlValor(v)}`);
      const sql = `select coalesce(row_to_json(t), 'null'::json) from public.${nome}(${partes.join(", ")}) t;`;
      const r = psql(`set role service_role; ${sql}`);
      if (!r.ok) {
        return { data: null, error: { message: r.stderr || r.stdout || "psql falhou" } };
      }
      return { data: JSON.parse(r.stdout), error: null };
    },
    from(tabela: string) {
      const filtros: string[] = [];
      const api = {
        select() {
          return api;
        },
        eq(col: string, val: unknown) {
          filtros.push(`${col} = ${sqlValor(val)}`);
          return api;
        },
        order(col: string, opts?: { ascending?: boolean }) {
          api._order = `${col} ${opts?.ascending === false ? "desc" : "asc"}`;
          return api;
        },
        _order: "",
        async maybeSingle() {
          const where = filtros.length ? `where ${filtros.join(" and ")}` : "";
          const r = psql(
            `set role service_role; select coalesce(row_to_json(t), 'null'::json) from (select * from public.${tabela} ${where} limit 1) t;`,
          );
          if (!r.ok) {
            return { data: null, error: { message: r.stderr || r.stdout } };
          }
          if (!r.stdout || r.stdout === "null") {
            return { data: null, error: null };
          }
          return { data: JSON.parse(r.stdout), error: null };
        },
        then(
          resolve: (v: { data: unknown; error: unknown }) => unknown,
          reject?: (e: unknown) => unknown,
        ) {
          const where = filtros.length ? `where ${filtros.join(" and ")}` : "";
          const order = api._order ? `order by ${api._order}` : "";
          const r = psql(
            `set role service_role; select coalesce(json_agg(t), '[]'::json) from (select * from public.${tabela} ${where} ${order}) t;`,
          );
          const resultado = r.ok
            ? { data: JSON.parse(r.stdout || "[]"), error: null }
            : { data: null, error: { message: r.stderr || r.stdout } };
          return Promise.resolve(resultado).then(resolve, reject);
        },
      };
      return api;
    },
  } as unknown as SupabaseClient;
}

describe.skipIf(!process.env.ACOES_RPC_LIVE)("cliente contra o composto nulo do Postgres ao vivo", () => {
  it("acaoDaRpc trata o json real do cluster como ausência", () => {
    const nulo = lerJson(process.env.ACOES_RPC_NULO_JSON);
    expect(nulo).toMatchObject({ id: null, tool: null });
    expect(acaoDaRpc(nulo)).toBeNull();
    const rejeitar = process.env.ACOES_RPC_NULO_REJEITAR_JSON;
    if (rejeitar) {
      expect(acaoDaRpc(lerJson(rejeitar))).toBeNull();
    }
  });

  it("reivindicar concorrente (ainda em executando) devolve null e não marca falhou", async () => {
    const criar = psql(`
      set role service_role;
      select 1 from public.acoes_criar(
        '${ACAO_EXEC}'::uuid,
        '${USUARIO_A}'::uuid,
        'pagar',
        '{"valor": 9}'::jsonb,
        '${TRACE}'::uuid,
        now(),
        now() + interval '1 day',
        null
      );
    `);
    expect(criar.ok, criar.stderr).toBe(true);

    const repo = repositorioAcoesSupabase(clienteViaPsql());
    const ganhou = await repo.reivindicar(ACAO_EXEC, USUARIO_A, new Date().toISOString(), 30_000);
    expect(ganhou).toMatchObject({ status: "executando", tool: "pagar" });

    const segundo = await repo.reivindicar(ACAO_EXEC, USUARIO_A, new Date().toISOString(), 30_000);
    expect(segundo).toBeNull();
    expect(await repo.buscar(ACAO_EXEC, USUARIO_A)).toMatchObject({
      status: "executando",
    });
    expect((await repo.auditoria(ACAO_EXEC)).map((e) => e.evento)).toEqual([
      "criada",
      "aprovada",
    ]);
  });

  it("rejeitar de outro usuário devolve null e não altera a pendente", async () => {
    const id = "77777777-7777-4777-8777-777777777777";
    const criar = psql(`
      set role service_role;
      select 1 from public.acoes_criar(
        '${id}'::uuid,
        '${USUARIO_A}'::uuid,
        'pagar',
        '{"valor": 3}'::jsonb,
        '${TRACE}'::uuid,
        now(),
        now() + interval '1 day',
        null
      );
    `);
    expect(criar.ok, criar.stderr).toBe(true);
    const repo = repositorioAcoesSupabase(clienteViaPsql());
    expect(await repo.rejeitar(id, USUARIO_B, new Date().toISOString())).toBeNull();
    expect(await repo.buscar(id, USUARIO_A)).toMatchObject({ status: "pendente" });
  });
});
