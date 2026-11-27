import { promptExemplo } from "@/src/agentes/prompts/exemplo";
import { definicaoSomar } from "@/src/agentes/tools/exemplo";
import {
  ErroAgente,
  executarAgente,
  modeloFalsoSomar,
  type ModeloAgente,
  type ResultadoAgente,
  type ToolRegistro,
} from "@/src/agentes/harness";
import { dadosAssistente } from "@/src/agentes/contrato";

export type PedidoExemplo = {
  objetivo: string;
  tools?: ToolRegistro[];
  modelo?: ModeloAgente;
};

export function modeloPadrao(): ModeloAgente {
  if (process.env.AGENT_MODELO_FALSO === "1") {
    return modeloFalsoSomar();
  }
  throw new ErroAgente(
    "ERRO_INTERNO",
    "Defina AGENT_MODELO_FALSO=1 ou configure o modelo do agente.",
  );
}

export async function executarExemplo(
  pedido: PedidoExemplo,
): Promise<ResultadoAgente<{ total: number }>> {
  return executarAgente({
    objetivo: `${promptExemplo}

${pedido.objetivo}`,
    tools: pedido.tools ?? [definicaoSomar],
    modelo: pedido.modelo ?? modeloPadrao(),
    saida: dadosAssistente,
  });
}
