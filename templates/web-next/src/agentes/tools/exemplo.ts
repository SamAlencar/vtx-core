import { z } from "zod";
import { somar } from "@/src/dominio/exemplo";

export const esquemaSomar = z.object({
  a: z.number(),
  b: z.number(),
});

/** Tool que chama o domínio. Schema Zod na borda. */
export function toolSomar(input: unknown): number {
  const dados = esquemaSomar.parse(input);
  return somar(dados.a, dados.b);
}
