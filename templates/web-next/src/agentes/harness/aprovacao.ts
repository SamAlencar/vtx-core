import { z } from "zod";
import type { AcaoPendente, RepositorioAcoes } from "@/src/agentes/memoria/acoes";
import { ErroAgente } from "./erros";
import { lerTimeoutMs, type ContextoTool, type ToolRegistro } from "./executar";

export type PedidoAprovacao = {
  repositorio: RepositorioAcoes;
  acaoId: string;
  usuarioId: string;
  tools: ToolRegistro[];
  timeoutMs?: number;
};

export type ResultadoAprovacao =
  | { tipo: "aprovada"; acao: AcaoPendente }
  /** A ação já tinha saído de `pendente`: devolve o que está gravado, sem reexecutar. */
  | { tipo: "ja_decidida"; acao: AcaoPendente };

function naoEncontrada(): ErroAgente {
  return new ErroAgente("ELEMENTO_NAO_ENCONTRADO", "Ação não encontrada.");
}

async function rodarComPrazo(
  def: ToolRegistro,
  input: unknown,
  timeoutMs: number,
): Promise<unknown> {
  const controlador = new AbortController();
  const executar = def.executar as (input: unknown, ctx: ContextoTool) => Promise<unknown> | unknown;
  let temporizador: ReturnType<typeof setTimeout> | undefined;
  const prazo = new Promise<never>((_, reject) => {
    temporizador = setTimeout(() => {
      controlador.abort();
      reject(new ErroAgente("TIMEOUT", "A tool excedeu o timeoutMs."));
    }, timeoutMs);
  });
  try {
    const dados = def.entrada.parse(input);
    const bruto = await Promise.race([
      Promise.resolve(executar(dados, { signal: controlador.signal })),
      prazo,
    ]);
    return def.saida.parse(bruto);
  } finally {
    clearTimeout(temporizador);
    controlador.abort();
  }
}

/**
 * Executa a tool crítica de uma ação pendente, no máximo uma vez. Quem perde a
 * corrida ou chega depois recebe `ja_decidida` com o resultado gravado.
 */
export async function aprovarAcao(pedido: PedidoAprovacao): Promise<ResultadoAprovacao> {
  const { repositorio, acaoId, usuarioId } = pedido;
  const em = new Date().toISOString();
  const acao = await repositorio.reivindicar(acaoId, usuarioId, em);
  if (!acao) {
    const atual = await repositorio.buscar(acaoId, usuarioId);
    if (!atual) {
      throw naoEncontrada();
    }
    return { tipo: "ja_decidida", acao: atual };
  }
  await repositorio.auditar({ acao_id: acaoId, usuario_id: usuarioId, evento: "aprovada", em });

  const def = pedido.tools.find((t) => t.nome === acao.tool && t.critica);
  let final: AcaoPendente;
  try {
    if (!def) {
      throw new ErroAgente("FUNCAO_DESCONHECIDA", `Tool crítica desconhecida: ${acao.tool}.`);
    }
    const resultado = await rodarComPrazo(def, acao.input, pedido.timeoutMs ?? lerTimeoutMs());
    final = await repositorio.concluir(acaoId, { status: "executada", resultado });
  } catch (erro) {
    const mensagem =
      erro instanceof z.ZodError
        ? z.prettifyError(erro)
        : erro instanceof Error
          ? erro.message
          : "Falha ao executar a tool.";
    final = await repositorio.concluir(acaoId, { status: "falhou", erro: mensagem });
  }
  await repositorio.auditar({
    acao_id: acaoId,
    usuario_id: usuarioId,
    evento: final.status === "executada" ? "executada" : "falhou",
    em: new Date().toISOString(),
  });
  return { tipo: "aprovada", acao: final };
}
