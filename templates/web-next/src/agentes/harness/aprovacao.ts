import { z } from "zod";
import type { AcaoPendente, RepositorioAcoes } from "@/src/agentes/memoria/acoes";
import { ErroAgente } from "./erros";
import {
  lerTimeoutMs,
  retomarAgente,
  type ContextoTool,
  type PedidoRetomada,
  type ResultadoAgente,
  type ToolRegistro,
} from "./executar";

export type PedidoAprovacao<Saida = unknown> = {
  repositorio: RepositorioAcoes;
  acaoId: string;
  usuarioId: string;
  tools: ToolRegistro[];
  timeoutMs?: number;
  /** Se presente, o harness continua o loop depois de executar a tool. */
  retomada?: PedidoRetomada<Saida>;
};

export type ResultadoAprovacao<Saida = unknown> =
  | { tipo: "aprovada"; acao: AcaoPendente; agente?: ResultadoAgente<Saida>; erro_retomada?: string }
  /** A ação já tinha saído de `pendente`: devolve o que está gravado, sem reexecutar. */
  | { tipo: "ja_decidida"; acao: AcaoPendente };

export type ResultadoRejeicao =
  | { tipo: "rejeitada"; acao: AcaoPendente }
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
 * corrida ou chega depois recebe `ja_decidida` com o resultado gravado. TTL
 * vencido e lease de `executando` expirado já foram aplicados no reivindicar
 * (`expirada` / `falhou`).
 */
export async function aprovarAcao<Saida = unknown>(
  pedido: PedidoAprovacao<Saida>,
): Promise<ResultadoAprovacao<Saida>> {
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

  const def = pedido.tools.find((t) => t.nome === acao.tool && t.critica);
  let final: AcaoPendente;
  try {
    if (!def) {
      throw new ErroAgente("FUNCAO_DESCONHECIDA", `Tool crítica desconhecida: ${acao.tool}.`);
    }
    const resultado = await rodarComPrazo(def, acao.input, pedido.timeoutMs ?? lerTimeoutMs());
    final = await repositorio.concluir(acaoId, { status: "executada", resultado });
  } catch (erro) {
    const atual = await repositorio.buscar(acaoId, usuarioId);
    if (atual && atual.status !== "executando") {
      // Outra via já fechou (lease, segundo clique mal cronometrado, etc.).
      // Não chama concluir de novo: evita 500 e auditoria duplicada ou perdida.
      return { tipo: "ja_decidida", acao: atual };
    }
    const mensagem =
      erro instanceof z.ZodError
        ? z.prettifyError(erro)
        : erro instanceof Error
          ? erro.message
          : "Falha ao executar a tool.";
    try {
      final = await repositorio.concluir(acaoId, { status: "falhou", erro: mensagem });
    } catch {
      const depois = await repositorio.buscar(acaoId, usuarioId);
      if (!depois) {
        throw naoEncontrada();
      }
      return { tipo: "ja_decidida", acao: depois };
    }
  }

  if (final.status !== "executada" || !pedido.retomada) {
    return { tipo: "aprovada", acao: final };
  }

  try {
    const agente = await retomarAgente(final, final.resultado, {
      ...pedido.retomada,
      aprovacao: pedido.retomada.aprovacao ?? {
        repositorio,
        usuarioId,
      },
    });
    return { tipo: "aprovada", acao: final, agente };
  } catch (erro) {
    const mensagem =
      erro instanceof ErroAgente
        ? erro.message
        : erro instanceof Error
          ? erro.message
          : "Falha ao retomar o agente.";
    return { tipo: "aprovada", acao: final, erro_retomada: mensagem };
  }
}

/** Recusa uma ação ainda `pendente`. Idempotente no sentido de não reabrir decisão. */
export async function rejeitarAcao(pedido: {
  repositorio: RepositorioAcoes;
  acaoId: string;
  usuarioId: string;
}): Promise<ResultadoRejeicao> {
  const em = new Date().toISOString();
  const acao = await pedido.repositorio.rejeitar(pedido.acaoId, pedido.usuarioId, em);
  if (!acao) {
    const atual = await pedido.repositorio.buscar(pedido.acaoId, pedido.usuarioId);
    if (!atual) {
      throw naoEncontrada();
    }
    return { tipo: "ja_decidida", acao: atual };
  }
  return { tipo: "rejeitada", acao };
}
