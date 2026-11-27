/**
 * Esboço de memória de sessão. A VTX-216 coloca as tabelas e o repositório.
 */
export type MensagemAgente = {
  papel: "usuario" | "assistente";
  texto: string;
};

export type SessaoAgente = {
  id: string;
  mensagens: MensagemAgente[];
};

export function sessaoVazia(id: string): SessaoAgente {
  return { id, mensagens: [] };
}
