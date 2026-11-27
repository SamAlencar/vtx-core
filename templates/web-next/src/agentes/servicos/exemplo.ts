import { promptExemplo } from "@/src/agentes/prompts/exemplo";
import { definicaoSomar } from "@/src/agentes/tools/exemplo";
import {
  ErroAgente,
  executarAgente,
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

export async function modeloPadrao(): Promise<ModeloAgente> {
  if (process.env.NODE_ENV !== "production") {
    if (process.env.AGENT_MODELO_FALSO === "1") {
      const { modeloFalsoSomar } = await import("@/src/agentes/harness/modelo-falso");
      return modeloFalsoSomar();
    }
  } else if (process.env.AGENT_MODELO_FALSO === "1") {
    throw new ErroAgente(
      "ERRO_INTERNO",
      "AGENT_MODELO_FALSO não é permitido em produção.",
    );
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
    sistema: promptExemplo,
    objetivo: pedido.objetivo,
    tools: pedido.tools ?? [definicaoSomar],
    modelo: pedido.modelo ?? (await modeloPadrao()),
    saida: dadosAssistente,
  });
}
