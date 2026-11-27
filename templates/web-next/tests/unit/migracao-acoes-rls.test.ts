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

  it("revoga escrita de authenticated e anon; concede só SELECT", () => {
    for (const tabela of ["acoes_pendentes", "acoes_auditoria"]) {
      expect(sql).toMatch(
        new RegExp(`revoke all on table public\\.${tabela} from public, anon, authenticated`, "i"),
      );
      expect(sql).toMatch(new RegExp(`grant select on table public\\.${tabela} to authenticated`, "i"));
      expect(sql).not.toMatch(new RegExp(`grant (all|insert|update|delete).*${tabela} to authenticated`, "i"));
    }
  });

  it("RPCs de escrita são security definer com search_path fixo e EXECUTE só para service_role", () => {
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
