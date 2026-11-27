import { supabaseAdmin } from "@/lib/supabase-admin";
import {
  repositorioAcoesEmMemoria,
  type OpcoesRepositorioAcoes,
  type RepositorioAcoes,
} from "./acoes";
import { repositorioAcoesSupabase } from "./acoes-supabase";

/**
 * Em produção: Supabase com service_role.
 * Sem service_role: memória por processo (a ação some com o processo → 404 na
 * aprovação — falha segura, nunca executa a tool crítica).
 *
 * Fica neste módulo para não criar import circular entre `acoes.ts` e
 * `acoes-supabase.ts`.
 */
export function criarRepositorioPadrao(
  admin: ReturnType<typeof supabaseAdmin> = supabaseAdmin(),
  opts: OpcoesRepositorioAcoes = {},
): RepositorioAcoes {
  if (admin) {
    return repositorioAcoesSupabase(admin, opts);
  }
  return repositorioAcoesEmMemoria(opts);
}

export const repositorioAcoesPadrao: RepositorioAcoes = criarRepositorioPadrao();
