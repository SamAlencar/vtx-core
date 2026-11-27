import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const raiz = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const sql = readFileSync(
  resolve(raiz, "supabase/migrations/20261127000000_acoes_pendentes.sql"),
  "utf8",
);

function politicas(texto: string): string[] {
  return [...texto.matchAll(/create policy[\s\S]*?;/gi)].map((m) => m[0].replace(/\s+/g, " "));
}

function funcoes(texto: string): string[] {
  return [...texto.matchAll(/create or replace function[\s\S]*?\$\$;/gi)].map((m) => m[0]);
}

describe("migração acoes_pendentes: RLS e escrita só no servidor", () => {
  it("ativa RLS nas duas tabelas", () => {
    expect(sql).toMatch(/alter table public\.acoes_pendentes enable row level security/i);
    expect(sql).toMatch(/alter table public\.acoes_auditoria enable row level security/i);
  });

  it("authenticated só tem policy de SELECT das próprias linhas; não insere, atualiza nem apaga", () => {
    const ps = politicas(sql);
    expect(ps.length).toBe(2);
    for (const p of ps) {
      expect(p).toMatch(/for select to authenticated/i);
      expect(p).toMatch(/usuario_id = \(select auth\.uid\(\)\)/i);
      expect(p).not.toMatch(/for (insert|update|delete)/i);
    }
    expect(sql).not.toMatch(/create policy\s+\S+\s+on public\.acoes_pendentes\s+for (insert|update|delete)/i);
    expect(sql).not.toMatch(/create policy\s+\S+\s+on public\.acoes_auditoria\s+for (insert|update|delete)/i);
  });

  it("concede SELECT por coluna (sem contexto_retomada) e mantém a view de leitura", () => {
    expect(sql).toMatch(
      /revoke all on table public\.acoes_pendentes from public, anon, authenticated/i,
    );
    expect(sql).not.toMatch(/grant select on table public\.acoes_pendentes to authenticated/i);
    const colunas = sql.match(
      /grant select \(([\s\S]*?)\) on table public\.acoes_pendentes to authenticated/i,
    )?.[1];
    expect(colunas).toBeTruthy();
    expect(colunas).not.toMatch(/contexto_retomada/i);
    for (const col of [
      "id",
      "usuario_id",
      "tool",
      "input",
      "status",
      "trace_id",
      "criado_em",
      "expira_em",
      "executando_em",
      "aprovado_por",
      "aprovado_em",
      "resultado",
      "erro",
    ]) {
      expect(colunas).toMatch(new RegExp(`\\b${col}\\b`));
    }
    expect(sql).toMatch(
      /create or replace view public\.acoes_pendentes_leitura\s+with \(security_invoker = true\)/i,
    );
    const view = sql.match(
      /create or replace view public\.acoes_pendentes_leitura[\s\S]*?;/i,
    )?.[0] ?? "";
    expect(view).toBeTruthy();
    expect(view).not.toMatch(/contexto_retomada/i);
    expect(sql).toMatch(/grant select on public\.acoes_pendentes_leitura to authenticated/i);

    expect(sql).toMatch(
      /revoke all on table public\.acoes_auditoria from public, anon, authenticated/i,
    );
    expect(sql).toMatch(/grant select on table public\.acoes_auditoria to authenticated/i);
    expect(sql).not.toMatch(/grant (all|insert|update|delete).*acoes_auditoria to authenticated/i);
  });

  it("RPCs de escrita são security definer com search_path fixo, EXECUTE só para service_role, e auditam reivindicar e concluir", () => {
    const nomes = [
      "acoes_auditar",
      "acoes_criar",
      "acoes_reivindicar",
      "acoes_concluir",
      "acoes_rejeitar",
    ];
    const fns = funcoes(sql);
    expect(fns.length).toBe(nomes.length);
    for (const fn of fns) {
      expect(fn).toMatch(/security definer/i);
      expect(fn).toMatch(/set search_path = pg_catalog, public/i);
    }
    const reivindicar = fns.find((f) => /function public\.acoes_reivindicar/i.test(f)) ?? "";
    expect(reivindicar).toMatch(/acoes_auditar\([^)]*'aprovada'/i);
    const concluir = fns.find((f) => /function public\.acoes_concluir/i.test(f)) ?? "";
    expect(concluir).toMatch(/acoes_auditar\(/i);
    expect(concluir).toMatch(/p_status/);
    for (const nome of nomes) {
      expect(sql).toMatch(
        new RegExp(`revoke all on function public\\.${nome}\\([^)]*\\) from public, anon, authenticated`, "i"),
      );
      expect(sql).toMatch(
        new RegExp(`grant execute on function public\\.${nome}\\([^)]*\\) to service_role`, "i"),
      );
      expect(sql).not.toMatch(
        new RegExp(`grant execute on function public\\.${nome}\\([^)]*\\) to (authenticated|anon|public)`, "i"),
      );
    }
  });

  it("o esquema inclui rejeitada, expirada, expira_em e executando_em", () => {
    expect(sql).toMatch(/'rejeitada',\s*'expirada'/);
    expect(sql).toMatch(/expira_em timestamptz not null/);
    expect(sql).toMatch(/executando_em timestamptz/);
  });
});
