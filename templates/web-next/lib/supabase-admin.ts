import "server-only";

import { createClient, type SupabaseClient } from "@supabase/supabase-js";

/**
 * Cliente service_role só no servidor. Nunca importe isto em código de browser.
 * Sem URL ou service role → null (falha segura: o repositório de ações não grava
 * no banco e cai no padrão em memória).
 *
 * A chave NÃO entra em `lib/env.ts` (`EnvPublico`): aquele módulo é o contrato
 * das variáveis públicas do template. Aqui lemos `process.env` direto.
 */
export function supabaseAdmin(): SupabaseClient | null {
  if (typeof window !== "undefined") {
    throw new Error("supabaseAdmin só pode ser usado no servidor.");
  }
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    return null;
  }
  return createClient(url, key, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
}
