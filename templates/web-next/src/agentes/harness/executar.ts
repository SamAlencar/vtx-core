/**
 * Esboço do ponto único de chamada ao modelo.
 * A VTX-177 substitui isto pelo harness de referência (AI SDK, modelo injetável).
 */
export type ResultadoAgente = {
  texto: string;
  trace_id: string;
};

export type PedidoAgente = {
  prompt: string;
  mensagem: string;
  tools?: Record<string, (input: unknown) => unknown>;
};

export async function executarAgente(pedido: PedidoAgente): Promise<ResultadoAgente> {
  void pedido.prompt;
  void pedido.tools;
  return {
    texto: pedido.mensagem,
    trace_id: "stub",
  };
}
