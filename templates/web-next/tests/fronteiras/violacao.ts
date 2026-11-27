/** Fixture de fronteira: simula src/dominio importando agentes e o SDK de modelo. */
import { generateText } from "ai";
import { executarAgente } from "@/src/agentes/harness/executar";

export function proibido() {
  return [generateText, executarAgente];
}
