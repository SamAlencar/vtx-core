import { NextResponse } from "next/server";
import { z } from "zod";
import { problema } from "@/lib/http/problema";
import { entradaAssistente, saidaAssistente } from "@/src/agentes/contrato";
import { ErroAgente, type CodigoErro } from "@/src/agentes/harness";
import { executarExemplo, type PedidoExemplo } from "@/src/agentes/servicos/exemplo";

const AGENTES = new Set(["exemplo"]);

type ContextoRota = { params: Promise<{ agente: string }> };

export type DepsRotaAgente = {
  executar?: (pedido: PedidoExemplo) => ReturnType<typeof executarExemplo>;
};

function statusDe(codigo: CodigoErro): number {
  if (codigo === "PARAMETRO_INVALIDO" || codigo === "REGRA_VIOLADA") {
    return 422;
  }
  if (codigo === "ELEMENTO_NAO_ENCONTRADO" || codigo === "FUNCAO_DESCONHECIDA") {
    return 404;
  }
  if (codigo === "TIMEOUT") {
    return 504;
  }
  return 500;
}

function tituloDe(codigo: CodigoErro): string {
  if (codigo === "PARAMETRO_INVALIDO") {
    return "Entrada inválida";
  }
  if (codigo === "TIMEOUT") {
    return "Tempo esgotado";
  }
  return "Falha no agente";
}

function respostaErro(erro: ErroAgente): Response {
  const status = statusDe(erro.codigo);
  return NextResponse.json(
    problema(status, tituloDe(erro.codigo), erro.message, "about:blank", {
      codigo: erro.codigo,
      trace_id: erro.trace_id,
    }),
    { status },
  );
}

export function criarPost(deps: DepsRotaAgente = {}) {
  const executar = deps.executar ?? executarExemplo;
  return async function POST(req: Request, ctx: ContextoRota): Promise<Response> {
    const { agente } = await ctx.params;
    if (!AGENTES.has(agente)) {
      return NextResponse.json(
        problema(404, "Agente desconhecido", `Não há agente "${agente}".`),
        { status: 404 },
      );
    }

    let bruto: unknown;
    try {
      bruto = await req.json();
    } catch {
      return NextResponse.json(
        problema(400, "JSON inválido", "O corpo precisa ser um JSON válido."),
        { status: 400 },
      );
    }

    const lido = entradaAssistente.safeParse(bruto);
    if (!lido.success) {
      return NextResponse.json(
        problema(422, "Entrada inválida", z.prettifyError(lido.error)),
        { status: 422 },
      );
    }

    try {
      const resultado = await executar({ objetivo: lido.data.objetivo });
      const corpo = saidaAssistente.parse({
        texto: resultado.texto,
        trace_id: resultado.trace_id,
        passos: resultado.passos,
        toolsChamadas: resultado.toolsChamadas,
        dados: resultado.dados,
      });
      return NextResponse.json(corpo);
    } catch (erro) {
      if (erro instanceof ErroAgente) {
        return respostaErro(erro);
      }
      const mensagem = erro instanceof Error ? erro.message : "Falha interna no agente.";
      return NextResponse.json(
        problema(500, "Falha no agente", mensagem, "about:blank", {
          codigo: "ERRO_INTERNO",
        }),
        { status: 500 },
      );
    }
  };
}

export const POST = criarPost();
