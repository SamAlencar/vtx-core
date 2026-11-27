import { NextResponse } from "next/server";
import { z } from "zod";
import { usuarioDaRequisicao, type Usuario } from "@/lib/auth";
import { problema } from "@/lib/http/problema";
import { ErroAgente, rejeitarAcao } from "@/src/agentes/harness";
import { type AcaoPendente, type RepositorioAcoes } from "@/src/agentes/memoria/acoes";
import { repositorioAcoesPadrao } from "@/src/agentes/memoria/acoes-padrao";
import { saidaAprovar } from "./aprovar";

type ContextoRota = { params: Promise<{ id: string }> };

export type DepsRotaRejeitar = {
  autenticar?: (req: Request) => Promise<Usuario | null>;
  repositorio?: RepositorioAcoes;
};

const entrada = z.object({ id: z.string().uuid() });

function corpoAcao(acao: AcaoPendente) {
  return saidaAprovar.parse({
    acao_id: acao.id,
    status: acao.status,
    tool: acao.tool,
    aprovado_por: acao.aprovado_por,
    aprovado_em: acao.aprovado_em,
    resultado: acao.resultado,
    erro: acao.erro,
  });
}

export function criarPostRejeitar(deps: DepsRotaRejeitar = {}) {
  const autenticar = deps.autenticar ?? usuarioDaRequisicao;
  const repositorio = deps.repositorio ?? repositorioAcoesPadrao;

  return async function POST(req: Request, ctx: ContextoRota): Promise<Response> {
    const usuario = await autenticar(req);
    if (!usuario) {
      return NextResponse.json(
        problema(401, "Não autenticado", "Envie Authorization: Bearer com a sessão do usuário."),
        { status: 401 },
      );
    }

    const lido = entrada.safeParse(await ctx.params);
    if (!lido.success) {
      return NextResponse.json(
        problema(422, "Entrada inválida", z.prettifyError(lido.error)),
        { status: 422 },
      );
    }

    try {
      const r = await rejeitarAcao({
        repositorio,
        acaoId: lido.data.id,
        usuarioId: usuario.id,
      });
      if (r.tipo === "ja_decidida") {
        return NextResponse.json(
          {
            ...problema(409, "Ação já decidida", `A ação está em ${r.acao.status}; não rejeita de novo.`),
            acao: corpoAcao(r.acao),
          },
          { status: 409 },
        );
      }
      return NextResponse.json(corpoAcao(r.acao));
    } catch (erro) {
      if (erro instanceof ErroAgente && erro.codigo === "ELEMENTO_NAO_ENCONTRADO") {
        return NextResponse.json(problema(404, "Ação não encontrada"), { status: 404 });
      }
      const trace_id = crypto.randomUUID();
      console.error(
        JSON.stringify({
          nivel: "error",
          origem: "rota-rejeitar",
          trace_id,
          mensagem: erro instanceof Error ? erro.message : String(erro),
        }),
      );
      return NextResponse.json(
        problema(
          500,
          "Falha na rejeição",
          `Falha interna. Informe o trace_id ${trace_id} se precisar de suporte.`,
          "about:blank",
          { codigo: "ERRO_INTERNO", trace_id },
        ),
        { status: 500 },
      );
    }
  };
}
