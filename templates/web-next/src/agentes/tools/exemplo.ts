import { z } from "zod";
import { somar } from "@/src/dominio/exemplo";
import type { ToolDefinicao } from "@/src/agentes/harness";

export const esquemaSomar = z.object({
  a: z.number(),
  b: z.number(),
});

/** Tool que chama o domínio. Schema Zod na borda. */
export function toolSomar(input: unknown): number {
  const dados = esquemaSomar.parse(input);
  return somar(dados.a, dados.b);
}

export const definicaoSomar: ToolDefinicao<{ a: number; b: number }, number> = {
  nome: "somar",
  descricao: "Soma dois números usando a regra de domínio.",
  entrada: esquemaSomar,
  saida: z.number(),
  executar: (dados) => somar(dados.a, dados.b),
};
