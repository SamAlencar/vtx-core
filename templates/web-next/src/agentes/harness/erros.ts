/** Códigos de `knowledge/engenharia/ia/funcoes-de-dominio.md` mais os do harness. */
export type CodigoErro =
  | "PARAMETRO_INVALIDO"
  | "ELEMENTO_NAO_ENCONTRADO"
  | "REGRA_VIOLADA"
  | "FUNCAO_DESCONHECIDA"
  | "ERRO_INTERNO"
  | "TIMEOUT"
  | "MAX_ITERACOES";

export class ErroAgente extends Error {
  readonly codigo: CodigoErro;
  readonly campo?: string;
  readonly trace_id?: string;

  constructor(codigo: CodigoErro, mensagem: string, campo?: string, trace_id?: string) {
    super(mensagem);
    this.name = "ErroAgente";
    this.codigo = codigo;
    if (campo) {
      this.campo = campo;
    }
    if (trace_id) {
      this.trace_id = trace_id;
    }
  }

  comTrace(trace_id: string): ErroAgente {
    if (this.trace_id) {
      return this;
    }
    return new ErroAgente(this.codigo, this.message, this.campo, trace_id);
  }
}

export function ehErroAgente(erro: unknown): erro is ErroAgente {
  return erro instanceof ErroAgente;
}
