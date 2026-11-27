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

  constructor(codigo: CodigoErro, mensagem: string, campo?: string) {
    super(mensagem);
    this.name = "ErroAgente";
    this.codigo = codigo;
    if (campo) {
      this.campo = campo;
    }
  }
}

export function ehErroAgente(erro: unknown): erro is ErroAgente {
  return erro instanceof ErroAgente;
}
