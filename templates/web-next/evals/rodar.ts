import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";
import { dadosAssistente } from "../src/agentes/contrato";
import { ErroAgente, executarAgente, type ToolDefinicao } from "../src/agentes/harness";
import { modeloGravado, type PassoGravado } from "../src/agentes/harness/modelo-falso";
import { promptExemplo } from "../src/agentes/prompts/exemplo";
import { definicaoSomar } from "../src/agentes/tools/exemplo";
import { avaliar, type Limiares, type Metricas } from "./avaliar";

const raiz = path.dirname(fileURLToPath(import.meta.url));

const casoSchema = z.object({
  id: z.string(),
  tipo: z.enum(["feliz", "recusa", "erro-tool", "argumento", "injecao"]),
  objetivo: z.string(),
  ferramenta: z.enum(["falha"]).optional(),
  roteiro: z.array(
    z.union([
      z.object({ tipo: z.literal("texto"), texto: z.string() }),
      z.object({ tipo: z.literal("tool"), nome: z.string(), input: z.unknown() }),
    ]),
  ),
  esperado: z.object({
    toolsChamadas: z.array(z.string()).optional(),
    schema: z.boolean().optional(),
    recusa: z.boolean().optional(),
    dados: z.unknown().optional(),
    codigo: z.string().optional(),
  }),
});

type Caso = z.infer<typeof casoSchema>;

const toolFalha: ToolDefinicao<{ a: number; b: number }, number> = {
  ...definicaoSomar,
  executar: () => {
    throw new Error("falha na tool de eval");
  },
};

async function lerCasos(): Promise<Caso[]> {
  const dir = path.join(raiz, "datasets");
  const nomes = (await readdir(dir)).filter((n) => n.endsWith(".jsonl")).sort();
  const casos: Caso[] = [];
  for (const nome of nomes) {
    const texto = await readFile(path.join(dir, nome), "utf8");
    for (const linha of texto.split("\n")) {
      if (!linha.trim()) continue;
      casos.push(casoSchema.parse(JSON.parse(linha)));
    }
  }
  return casos;
}

function lerLimiares(caminho: string): Promise<Limiares> {
  return readFile(caminho, "utf8").then((t) => JSON.parse(t) as Limiares);
}

type Detalhe = {
  id: string;
  tipo: Caso["tipo"];
  ok: boolean;
  passos?: number;
  toolsChamadas?: string[];
  codigo?: string;
  motivo?: string;
};

async function rodarCaso(caso: Caso): Promise<Detalhe> {
  const tools = caso.ferramenta === "falha" ? [toolFalha] : [definicaoSomar];
  try {
    const resultado = await executarAgente({
      sistema: promptExemplo,
      objetivo: caso.objetivo,
      tools,
      modelo: modeloGravado(caso.roteiro as PassoGravado[]),
      saida: caso.esperado.schema ? dadosAssistente : undefined,
      maxIteracoes: 4,
      timeoutMs: 5000,
      esperar: async () => undefined,
    });
    if (caso.esperado.codigo) {
      return { id: caso.id, tipo: caso.tipo, ok: false, motivo: "esperava erro e obteve sucesso" };
    }
    if (caso.esperado.toolsChamadas) {
      const iguais =
        JSON.stringify(resultado.toolsChamadas) === JSON.stringify(caso.esperado.toolsChamadas);
      if (!iguais) {
        return {
          id: caso.id,
          tipo: caso.tipo,
          ok: false,
          passos: resultado.passos,
          toolsChamadas: resultado.toolsChamadas,
          motivo: "toolsChamadas divergentes",
        };
      }
    }
    if (caso.esperado.recusa && resultado.toolsChamadas.length > 0) {
      return {
        id: caso.id,
        tipo: caso.tipo,
        ok: false,
        toolsChamadas: resultado.toolsChamadas,
        motivo: "recusa deveria ocorrer sem tool",
      };
    }
    if (caso.esperado.schema && caso.esperado.dados !== undefined) {
      if (JSON.stringify(resultado.dados) !== JSON.stringify(caso.esperado.dados)) {
        return { id: caso.id, tipo: caso.tipo, ok: false, motivo: "dados divergentes do schema" };
      }
    }
    return {
      id: caso.id,
      tipo: caso.tipo,
      ok: true,
      passos: resultado.passos,
      toolsChamadas: resultado.toolsChamadas,
    };
  } catch (erro) {
    const codigo = erro instanceof ErroAgente ? erro.codigo : "ERRO_INTERNO";
    if (caso.esperado.codigo && codigo === caso.esperado.codigo) {
      return { id: caso.id, tipo: caso.tipo, ok: true, codigo };
    }
    return {
      id: caso.id,
      tipo: caso.tipo,
      ok: false,
      codigo,
      motivo: erro instanceof Error ? erro.message : "erro inesperado",
    };
  }
}

function metricasDe(casos: Caso[], detalhes: Detalhe[]): Metricas {
  const taxa = (pred: (c: Caso, d: Detalhe) => boolean | undefined) => {
    const pares = casos
      .map((c, i) => [c, detalhes[i]] as const)
      .filter(([c, d]) => pred(c, d) !== undefined);
    if (pares.length === 0) return 1;
    const ok = pares.filter(([c, d]) => pred(c, d) === true).length;
    return ok / pares.length;
  };
  const acerto_tool = taxa((c, d) =>
    c.esperado.toolsChamadas ? d.ok && JSON.stringify(d.toolsChamadas) === JSON.stringify(c.esperado.toolsChamadas) : undefined,
  );
  const validade_schema = taxa((c, d) => {
    if (c.esperado.schema) return d.ok;
    if (c.esperado.codigo) return d.ok && d.codigo === c.esperado.codigo;
    return undefined;
  });
  const recusa_correta = taxa((c, d) => (c.esperado.recusa ? d.ok : undefined));
  const comPassos = detalhes.filter((d) => typeof d.passos === "number");
  const passos_medio =
    comPassos.length === 0
      ? 0
      : comPassos.reduce((s, d) => s + (d.passos ?? 0), 0) / comPassos.length;
  return { acerto_tool, validade_schema, recusa_correta, passos_medio };
}

export async function rodarEvals(opts?: { limiares?: string; saida?: string }) {
  const caminhoLimiares = opts?.limiares ?? process.env.EVALS_LIMIARES ?? path.join(raiz, "limiares.json");
  const caminhoSaida = opts?.saida ?? path.join(raiz, "resultado.json");
  const casos = await lerCasos();
  const detalhes: Detalhe[] = [];
  for (const caso of casos) {
    detalhes.push(await rodarCaso(caso));
  }
  const metricas = metricasDe(casos, detalhes);
  const limiares = await lerLimiares(caminhoLimiares);
  const falhas = avaliar(metricas, limiares);
  const relatorio = {
    casos: casos.length,
    metricas,
    limiares,
    ok: falhas.length === 0 && detalhes.every((d) => d.ok),
    falhas,
    detalhes,
  };
  await writeFile(caminhoSaida, JSON.stringify(relatorio, null, 2) + "\n", "utf8");
  return { relatorio, caminhoSaida };
}

