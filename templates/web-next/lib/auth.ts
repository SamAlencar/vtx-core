import { createClient } from "@supabase/supabase-js";
import { lerEnv } from "./env";

export type Usuario = { id: string };

/**
 * Usuário do header `Authorization: Bearer <jwt do Supabase>`, validado em
 * `auth.getUser`. Sem env do Supabase ou sem token válido devolve null (401).
 */
export async function usuarioDaRequisicao(req: Request): Promise<Usuario | null> {
  const cabecalho = req.headers.get("authorization") ?? "";
  const m = cabecalho.match(/^Bearer\s+(.+)$/i);
  if (!m) {
    return null;
  }
  const env = lerEnv();
  if (!env.NEXT_PUBLIC_SUPABASE_URL || !env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
    return null;
  }
  const cliente = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.NEXT_PUBLIC_SUPABASE_ANON_KEY, {
    auth: { persistSession: false },
  });
  const { data, error } = await cliente.auth.getUser(m[1]);
  if (error || !data.user) {
    return null;
  }
  return { id: data.user.id };
}
