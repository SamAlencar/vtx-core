/**
 * Ações pendentes de tools críticas (VTX-213). A tabela em Supabase está em
 * `supabase/migrations/20261127000000_acoes_pendentes.sql`, com RLS por usuário.
 */
export type StatusAcao = "pendente" | "executando" | "executada" | "falhou";

export type AcaoPendente = {
  id: string;
  usuario_id: string;
  tool: string;
  input: unknown;
  status: StatusAcao;
  trace_id: string;
  criado_em: string;
  aprovado_por?: string;
  aprovado_em?: string;
  resultado?: unknown;
  erro?: string;
};

export type EventoAuditoria = "criada" | "aprovada" | "executada" | "falhou";

export type RegistroAuditoria = {
  acao_id: string;
  usuario_id: string;
  evento: EventoAuditoria;
  em: string;
};

export type DesfechoAcao =
  | { status: "executada"; resultado: unknown }
  | { status: "falhou"; erro: string };

export interface RepositorioAcoes {
  criar(acao: AcaoPendente): Promise<void>;
  /** Só devolve a ação do próprio usuário (o RLS faz o mesmo no banco). */
  buscar(id: string, usuarioId: string): Promise<AcaoPendente | null>;
  /**
   * Troca `pendente` por `executando` de forma atômica. Devolve a ação se esta
   * chamada ganhou; `null` se não existe, é de outro usuário ou já saiu de `pendente`.
   */
  reivindicar(id: string, usuarioId: string, em: string): Promise<AcaoPendente | null>;
  concluir(id: string, desfecho: DesfechoAcao): Promise<AcaoPendente>;
  auditar(registro: RegistroAuditoria): Promise<void>;
  auditoria(acaoId: string): Promise<RegistroAuditoria[]>;
}

/** Implementação em memória, para testes e para o modelo falso em desenvolvimento. */
export function repositorioAcoesEmMemoria(): RepositorioAcoes {
  const acoes = new Map<string, AcaoPendente>();
  const registros: RegistroAuditoria[] = [];
  const copia = (a: AcaoPendente): AcaoPendente => structuredClone(a);

  return {
    async criar(acao) {
      acoes.set(acao.id, copia(acao));
    },
    async buscar(id, usuarioId) {
      const a = acoes.get(id);
      return a && a.usuario_id === usuarioId ? copia(a) : null;
    },
    async reivindicar(id, usuarioId, em) {
      const a = acoes.get(id);
      if (!a || a.usuario_id !== usuarioId || a.status !== "pendente") {
        return null;
      }
      a.status = "executando";
      a.aprovado_por = usuarioId;
      a.aprovado_em = em;
      return copia(a);
    },
    async concluir(id, desfecho) {
      const a = acoes.get(id);
      if (!a) {
        throw new Error(`ação ${id} não existe`);
      }
      a.status = desfecho.status;
      if (desfecho.status === "executada") {
        a.resultado = desfecho.resultado;
      } else {
        a.erro = desfecho.erro;
      }
      return copia(a);
    },
    async auditar(registro) {
      registros.push({ ...registro });
    },
    async auditoria(acaoId) {
      return registros.filter((r) => r.acao_id === acaoId).map((r) => ({ ...r }));
    },
  };
}

/**
 * Repositório padrão da rota de aprovação. Em memória por processo: em produção
 * troque por um repositório Supabase com o cliente do usuário (RLS). Sem isso,
 * a ação some com o processo e a aprovação responde 404 — falha segura, nunca executa.
 */
export const repositorioAcoesPadrao: RepositorioAcoes = repositorioAcoesEmMemoria();
