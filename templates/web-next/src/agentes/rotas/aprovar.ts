import { NextResponse } from "next/server";
import { z } from "zod";
import { usuarioDaRequisicao, type Usuario } from "@/lib/auth";
import { problema } from "@/lib/http/problema";
import { aprovarAcao, ErroAgente, type ToolRegistro } from "@/src/agentes/harness";
import { repositorioAcoesPadrao, type AcaoPendente, type RepositorioAcoes } from "@/src/agentes/memoria/acoes";
import { catalogoTools } from "@/src/agentes/tools/catalogo";

type ContextoRota = { params: Promise<{ id: string }> };

export type DepsRotaAprovar = {
  autenticar?: (req: Request) => Promise<Usuario | null>;
  repositorio?: RepositorioAcoes;
  tools?: ToolRegistro[];
};

const entrada = z.object({ id: z.string().uuid() });

export const saidaAprovar = z.object({
  acao_id: z.string().uuid(),
  status: z.enum(["pendente", "executando", "executada", "falhou"]),
  tool: z.string(),
  aprovado_por: z.string().optional(),
  aprovado_em: z.string().optional(),
  resultado: z.unknown().optional(),
  erro: z.string().optional(),
});

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

export function criarPostAprovar(deps: DepsRotaAprovar = {}) {
  const autenticar = deps.autenticar ?? usuarioDaRequisicao;
  const repositorio = deps.repositorio ?? repositorioAcoesPadrao;
  const tools = deps.tools ?? catalogoTools;

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
      const r = await aprovarAcao({
        repositorio,
        acaoId: lido.data.id,
        usuarioId: usuario.id,
        tools,
      });
      if (r.tipo === "ja_decidida") {
        return NextResponse.json(
          {
            ...problema(409, "Ação já decidida", `A ação está em ${r.acao.status}; não executa de novo.`),
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
          origem: "rota-aprovar",
          trace_id,
          mensagem: erro instanceof Error ? erro.message : String(erro),
        }),
      );
      return NextResponse.json(
        problema(
          500,
          "Falha na aprovação",
          `Falha interna. Informe o trace_id ${trace_id} se precisar de suporte.`,
          "about:blank",
          { codigo: "ERRO_INTERNO", trace_id },
        ),
        { status: 500 },
      );
    }
  };
}
