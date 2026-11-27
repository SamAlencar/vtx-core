import { NextResponse } from "next/server";
import { z } from "zod";
import { problema } from "@/lib/http/problema";

const entrada = z.object({ mensagem: z.string().min(1) });
const saida = z.object({ eco: z.string() });

export async function postExemplo(req: Request): Promise<Response> {
  const bruto: unknown = await req.json();
  const lido = entrada.safeParse(bruto);
  if (!lido.success) {
    return NextResponse.json(
      problema(422, "Entrada inválida", lido.error.message),
      { status: 422 },
    );
  }
  const corpo = saida.parse({ eco: lido.data.mensagem });
  return NextResponse.json(corpo);
}
