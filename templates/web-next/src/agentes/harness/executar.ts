import {
  APICallError,
  generateText,
  InvalidToolInputError,
  NoSuchToolError,
  tool,
  type LanguageModel,
} from "ai";
import { z } from "zod";
import { ErroAgente } from "./erros";

export type ModeloAgente = LanguageModel;

export type ToolDefinicao<Entrada = unknown, Saida = unknown> = {
  nome: string;
  descricao: string;
  entrada: z.ZodType<Entrada>;
  saida: z.ZodType<Saida>;
  executar: (input: Entrada) => Promise<Saida> | Saida;
};

/** Versão apagada para listas heterogêneas (parâmetro de executar é contravariante). */
export type ToolRegistro = {
  nome: string;
  descricao: string;
  entrada: z.ZodType;
  saida: z.ZodType;
  executar: (input: never) => Promise<unknown> | unknown;
};

export type PedidoAgente<Saida = unknown> = {
  objetivo: string;
  tools: ToolRegistro[];
  modelo: ModeloAgente;
  maxIteracoes?: number;
  /** Prazo da execução inteira, inclusive das tools — não só da chamada ao modelo. */
  timeoutMs?: number;
  /**
   * Modelo alternativo se o principal falhar, inclusive em erro não transitório
   * (por exemplo 401). Erro transitório (429, 5xx, isRetryable) ainda tenta
   * retry com backoff no modelo corrente antes de trocar.
   */
  fallback?: ModeloAgente;
  saida?: z.ZodType<Saida>;
  /** Só para testes: substitui o atraso do backoff. */
  esperar?: (ms: number) => Promise<void>;
};

export type ResultadoAgente<Saida = unknown> = {
  texto: string;
  trace_id: string;
  passos: number;
  toolsChamadas: string[];
  dados?: Saida;
};

const MAX_STEPS_PADRAO = 8;
const TIMEOUT_PADRAO_MS = 30_000;
const TENTATIVAS_TRANSITORIAS = 3;

export function lerMaxIteracoes(): number {
  const bruto = Number(process.env.AGENT_MAX_STEPS);
  return Number.isFinite(bruto) && bruto > 0 ? bruto : MAX_STEPS_PADRAO;
}

export function lerTimeoutMs(): number {
  const bruto = Number(process.env.AGENT_TIMEOUT_MS);
  return Number.isFinite(bruto) && bruto > 0 ? bruto : TIMEOUT_PADRAO_MS;
}

function campoDe(erro: unknown): string {
  const fila: unknown[] = [erro];
  const vistos = new Set<unknown>();
  while (fila.length > 0) {
    const atual = fila.shift();
    if (!atual || typeof atual !== "object" || vistos.has(atual)) {
      continue;
    }
    vistos.add(atual);
    const rec = atual as Record<string, unknown>;
    if (Array.isArray(rec.path) && rec.path.length > 0) {
      return String(rec.path[0]);
    }
    if (Array.isArray(rec.issues)) {
      fila.push(...rec.issues);
    }
    if ("cause" in rec) {
      fila.push(rec.cause);
    }
  }
  const msg = erro instanceof Error ? erro.message : "";
  const m = msg.match(/"path":\s*\[\s*"([^"]+)"/);
  if (m) {
    return m[1];
  }
  return "entrada";
}

function ehTransitorio(erro: unknown): boolean {
  if (APICallError.isInstance(erro)) {
    if (erro.isRetryable) {
      return true;
    }
    const status = erro.statusCode ?? 0;
    return status === 429 || status >= 500;
  }
  return false;
}

async function dormir(ms: number, esperar?: (ms: number) => Promise<void>) {
  if (esperar) {
    await esperar(ms);
    return;
  }
  await new Promise((ok) => setTimeout(ok, ms));
}

/** Encerra com TIMEOUT se o signal disparar enquanto a promessa ainda corre. */
async function comTimeout<T>(promessa: Promise<T>, signal: AbortSignal): Promise<T> {
  if (signal.aborted) {
    throw new ErroAgente("TIMEOUT", "A execução excedeu o timeoutMs.");
  }
  return await new Promise<T>((resolve, reject) => {
    const aoAbortar = () => {
      signal.removeEventListener("abort", aoAbortar);
      reject(new ErroAgente("TIMEOUT", "A execução excedeu o timeoutMs."));
    };
    signal.addEventListener("abort", aoAbortar, { once: true });
    promessa.then(
      (valor) => {
        signal.removeEventListener("abort", aoAbortar);
        resolve(valor);
      },
      (erro) => {
        signal.removeEventListener("abort", aoAbortar);
        reject(erro);
      },
    );
  });
}

function ferramentasSdk(tools: ToolRegistro[]) {
  return Object.fromEntries(
    tools.map((t) => [
      t.nome,
      tool({
        description: t.descricao,
        inputSchema: t.entrada,
      }),
    ]),
  );
}

type Mensagem = Parameters<typeof generateText>[0] extends { messages?: infer M }
  ? M extends (infer I)[]
    ? I
    : never
  : never;

async function gerarPasso(args: {
  modelo: ModeloAgente;
  mensagens: Mensagem[];
  tools: ToolRegistro[];
  signal: AbortSignal;
  esperar?: (ms: number) => Promise<void>;
  fallback?: ModeloAgente;
}) {
  const tentar = async (modelo: ModeloAgente) =>
    generateText({
      model: modelo,
      messages: args.mensagens,
      tools: ferramentasSdk(args.tools),
      abortSignal: args.signal,
      maxRetries: 0,
    });

  const chamarComRetry = async (modelo: ModeloAgente) => {
    let ultimo: unknown;
    for (let n = 0; n < TENTATIVAS_TRANSITORIAS; n += 1) {
      try {
        return await tentar(modelo);
      } catch (erro) {
        if (args.signal.aborted || erro instanceof ErroAgente && erro.codigo === "TIMEOUT") {
          throw new ErroAgente("TIMEOUT", "A execução excedeu o timeoutMs.");
        }
        ultimo = erro;
        if (!ehTransitorio(erro) || n === TENTATIVAS_TRANSITORIAS - 1) {
          break;
        }
        await dormir(10 * 2 ** n, args.esperar);
      }
    }
    throw ultimo;
  };

  try {
    return await chamarComRetry(args.modelo);
  } catch (erro) {
    if (erro instanceof ErroAgente) {
      throw erro;
    }
    if (args.signal.aborted) {
      throw new ErroAgente("TIMEOUT", "A execução excedeu o timeoutMs.");
    }
    if (args.fallback) {
      try {
        return await chamarComRetry(args.fallback);
      } catch (erroFallback) {
        if (erroFallback instanceof ErroAgente) {
          throw erroFallback;
        }
        if (args.signal.aborted) {
          throw new ErroAgente("TIMEOUT", "A execução excedeu o timeoutMs.");
        }
        throw new ErroAgente(
          "ERRO_INTERNO",
          erroFallback instanceof Error ? erroFallback.message : "Falha ao chamar o modelo.",
        );
      }
    }
    throw new ErroAgente(
      "ERRO_INTERNO",
      erro instanceof Error ? erro.message : "Falha ao chamar o modelo.",
    );
  }
}

function validarSaida<Saida>(texto: string, saida?: z.ZodType<Saida>): Saida | undefined {
  if (!saida) {
    return undefined;
  }
  let bruto: unknown = { texto };
  try {
    bruto = JSON.parse(texto) as unknown;
  } catch {
    bruto = { texto };
  }
  const lido = saida.safeParse(bruto);
  if (!lido.success) {
    throw new ErroAgente("ERRO_INTERNO", z.prettifyError(lido.error));
  }
  return lido.data;
}

export async function executarAgente<Saida = unknown>(
  pedido: PedidoAgente<Saida>,
): Promise<ResultadoAgente<Saida>> {
  const maxIteracoes = pedido.maxIteracoes ?? lerMaxIteracoes();
  const timeoutMs = pedido.timeoutMs ?? lerTimeoutMs();
  const trace_id = crypto.randomUUID();
  const toolsChamadas: string[] = [];
  const inicio = Date.now();
  const controlador = new AbortController();
  const temporizador = setTimeout(() => controlador.abort(), timeoutMs);

  const mensagens: Mensagem[] = [
    { role: "user", content: pedido.objetivo } as Mensagem,
  ];

  try {
    for (let passo = 1; passo <= maxIteracoes; passo += 1) {
      if (Date.now() - inicio >= timeoutMs || controlador.signal.aborted) {
        throw new ErroAgente("TIMEOUT", "A execução excedeu o timeoutMs.");
      }
      const gerado = await gerarPasso({
        modelo: pedido.modelo,
        mensagens,
        tools: pedido.tools,
        signal: controlador.signal,
        esperar: pedido.esperar,
        fallback: pedido.fallback,
      });

      const chamadas = gerado.toolCalls ?? [];
      const invalida = chamadas.find((c) => "invalid" in c && c.invalid);
      if (invalida && "error" in invalida) {
        const erro = invalida.error;
        if (NoSuchToolError.isInstance(erro)) {
          throw new ErroAgente(
            "FUNCAO_DESCONHECIDA",
            `Ferramenta desconhecida: ${invalida.toolName}.`,
          );
        }
        if (InvalidToolInputError.isInstance(erro)) {
          throw new ErroAgente(
            "PARAMETRO_INVALIDO",
            erro.message,
            campoDe(erro),
          );
        }
        throw new ErroAgente("ERRO_INTERNO", erro instanceof Error ? erro.message : "Tool inválida.");
      }

      if (chamadas.length === 0) {
        const texto = gerado.text;
        const dados = validarSaida(texto, pedido.saida);
        return { texto, trace_id, passos: passo, toolsChamadas, dados };
      }

      const resultados: Array<{
        type: "tool-result";
        toolCallId: string;
        toolName: string;
        output: unknown;
      }> = [];

      for (const chamada of chamadas) {
        const def = pedido.tools.find((t) => t.nome === chamada.toolName);
        if (!def) {
          throw new ErroAgente(
            "FUNCAO_DESCONHECIDA",
            `Ferramenta desconhecida: ${chamada.toolName}.`,
          );
        }
        toolsChamadas.push(chamada.toolName);
        try {
          const executar = def.executar as (input: unknown) => Promise<unknown> | unknown;
          const bruto = await comTimeout(Promise.resolve(executar(chamada.input)), controlador.signal);
          const saidaTool = def.saida.parse(bruto);
          resultados.push({
            type: "tool-result",
            toolCallId: chamada.toolCallId,
            toolName: chamada.toolName,
            output: saidaTool,
          });
        } catch (erro) {
          if (erro instanceof ErroAgente) {
            throw erro;
          }
          if (erro instanceof z.ZodError) {
            throw new ErroAgente("ERRO_INTERNO", z.prettifyError(erro));
          }
          throw new ErroAgente(
            "ERRO_INTERNO",
            erro instanceof Error ? erro.message : "Falha ao executar a tool.",
          );
        }
      }

      mensagens.push(...(gerado.response.messages as Mensagem[]));
      mensagens.push({
        role: "tool",
        content: resultados,
      } as Mensagem);
    }

    throw new ErroAgente(
      "MAX_ITERACOES",
      `Parou em maxIteracoes (${maxIteracoes}).`,
    );
  } catch (erro) {
    if (erro instanceof ErroAgente) {
      throw erro.comTrace(trace_id);
    }
    if (controlador.signal.aborted) {
      throw new ErroAgente("TIMEOUT", "A execução excedeu o timeoutMs.", undefined, trace_id);
    }
    throw new ErroAgente(
      "ERRO_INTERNO",
      erro instanceof Error ? erro.message : "Falha interna no harness.",
      undefined,
      trace_id,
    );
  } finally {
    clearTimeout(temporizador);
  }
}

export type { CodigoErro } from "./erros";
export { ErroAgente, ehErroAgente } from "./erros";
