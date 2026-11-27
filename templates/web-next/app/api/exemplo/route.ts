import { NextResponse } from "next/server";
import { z } from "zod";
import { problema } from "@/lib/http/problema";

const entrada = z.object({ mensagem: z.string().min(1) });
const saida = z.object({ eco: z.string() });

/** Esboço de Route Handler com schema de entrada e de saída. */
export async function POST(req: Request): Promise<Response> {
  let bruto: unknown;
  try {
    bruto = await req.json();
  } catch {
    return NextResponse.json(
      problema(400, "JSON inválido", "O corpo precisa ser um JSON válido."),
      { status: 400 },
    );
  }
  const lido = entrada.safeParse(bruto);
  if (!lido.success) {
    return NextResponse.json(
      problema(422, "Entrada inválida", z.prettifyError(lido.error)),
      { status: 422 },
    );
  }
  const corpo = saida.parse({ eco: lido.data.mensagem });
  return NextResponse.json(corpo);
}
