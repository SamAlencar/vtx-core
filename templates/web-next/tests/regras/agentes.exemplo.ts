import { z } from "zod";
import { promptExemplo } from "@/src/agentes/prompts/exemplo";
import { somar } from "@/src/dominio/exemplo";
import {
  executarAgente,
  type ModeloAgente,
  type ToolDefinicao,
} from "@/src/agentes/harness";

const esquemaSomar = z.object({ a: z.number(), b: z.number() });

export const definicaoSomar: ToolDefinicao<{ a: number; b: number }, number> = {
  nome: "somar",
  descricao: "Soma dois números.",
  entrada: esquemaSomar,
  saida: z.number(),
  executar: (dados) => somar(dados.a, dados.b),
};

export async function demonstracaoHarness(modelo: ModeloAgente) {
  return executarAgente({
    sistema: promptExemplo,
    objetivo: "Some 1 e 2.",
    tools: [definicaoSomar],
    modelo,
    saida: z.object({ total: z.number() }),
  });
}
