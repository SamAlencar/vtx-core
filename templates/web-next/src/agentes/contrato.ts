import { z } from "zod";

/** Contrato compartilhado entre a rota, o serviço e a tela do assistente. */
export const entradaAssistente = z.object({
  objetivo: z.string().min(1).max(4000),
});

export const dadosAssistente = z.object({
  total: z.number(),
});

export const saidaAssistente = z.object({
  texto: z.string(),
  trace_id: z.string().uuid(),
  passos: z.number().int().positive(),
  toolsChamadas: z.array(z.string()),
  dados: dadosAssistente.optional(),
});

export type EntradaAssistente = z.infer<typeof entradaAssistente>;
export type SaidaAssistente = z.infer<typeof saidaAssistente>;
