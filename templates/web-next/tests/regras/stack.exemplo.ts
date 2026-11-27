import { z } from "zod";
import { problema } from "@/lib/http/problema";

const entrada = z.object({ nome: z.string().min(1) });

export function validarNome(bruto: unknown) {
  const lido = entrada.safeParse(bruto);
  if (!lido.success) {
    return { ok: false as const, problema: problema(422, "Entrada inválida", lido.error.message) };
  }
  return { ok: true as const, nome: lido.data.nome };
}
