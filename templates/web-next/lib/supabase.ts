import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { lerEnv } from "./env";

/** Cliente de browser só quando URL e chave anônima existem. Sem segredo de serviço aqui. */
export function supabaseBrowser(): SupabaseClient | null {
  const env = lerEnv();
  if (!env.NEXT_PUBLIC_SUPABASE_URL || !env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
    return null;
  }
  return createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.NEXT_PUBLIC_SUPABASE_ANON_KEY);
}
