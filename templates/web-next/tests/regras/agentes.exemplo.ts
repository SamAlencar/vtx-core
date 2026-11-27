import { z } from "zod";
import { promptExemplo } from "@/src/agentes/prompts/exemplo";
import { somar } from "@/src/dominio/exemplo";
import { executarAgente } from "@/src/agentes/harness/executar";

const esquemaSomar = z.object({ a: z.number(), b: z.number() });

export function toolSomar(input: unknown): number {
  const dados = esquemaSomar.parse(input);
  return somar(dados.a, dados.b);
}

export async function demonstracaoHarness() {
  return executarAgente({
    prompt: promptExemplo,
    mensagem: "some 1 e 2",
    tools: { somar: toolSomar },
  });
}
