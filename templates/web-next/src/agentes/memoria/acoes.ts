/**
 * Ações pendentes de tools críticas (VTX-213 / VTX-230).
 *
 * A tabela está em `supabase/migrations/20261127000000_acoes_pendentes.sql`.
 * Quem escreve (insert/update/delete e auditoria) é o servidor, via
 * service_role ou RPC `security definer` com search_path fixo e EXECUTE só
 * para service_role. O RLS do papel `authenticated` protege só a leitura
 * (SELECT das próprias linhas). A implementação Supabase está em
 * `acoes-supabase.ts`; o padrão das rotas (`acoes-padrao.ts`) escolhe
 * Supabase se houver service_role, senão memória por processo.
 */
export type StatusAcao =
  | "pendente"
  | "executando"
  | "executada"
  | "falhou"
  | "rejeitada"
  | "expirada";

export type ContextoRetomada = {
  mensagens: unknown[];
  mensagensAssistente: unknown[];
  resultadosParciais: Array<{
    type: "tool-result";
    toolCallId: string;
    toolName: string;
    output: unknown;
  }>;
  toolCallId: string;
  passo: number;
  toolsChamadas: string[];
  maxIteracoes: number;
  sistema?: string;
};

export type AcaoPendente = {
  id: string;
  usuario_id: string;
  tool: string;
  input: unknown;
  status: StatusAcao;
  trace_id: string;
  criado_em: string;
  expira_em: string;
  executando_em?: string;
  contexto_retomada?: ContextoRetomada;
  aprovado_por?: string;
  aprovado_em?: string;
  resultado?: unknown;
  erro?: string;
};

export type EventoAuditoria =
  | "criada"
  | "aprovada"
  | "executada"
  | "falhou"
  | "rejeitada"
  | "expirada";

export type RegistroAuditoria = {
  acao_id: string;
  usuario_id: string;
  evento: EventoAuditoria;
  em: string;
};

export type DesfechoAcao =
  | { status: "executada"; resultado: unknown }
  | { status: "falhou"; erro: string };

export const ACAO_TTL_PADRAO_MS = 24 * 60 * 60 * 1000;
/** Folga além do timeout da tool, para o segundo clique não encerrar a execução ainda em curso. */
export const ACAO_LEASE_MARGEM_MS = 10_000;
const TIMEOUT_PADRAO_MS = 30_000;

/** Lease = timeout da tool (AGENT_TIMEOUT_MS ou o informado) + margem. */
export function leaseMsDeTimeout(timeoutMs: number): number {
  return timeoutMs + ACAO_LEASE_MARGEM_MS;
}

function timeoutAtualMs(): number {
  const bruto = Number(process.env.AGENT_TIMEOUT_MS);
  return Number.isFinite(bruto) && bruto > 0 ? bruto : TIMEOUT_PADRAO_MS;
}

export type OpcoesRepositorioAcoes = {
  /** Relógio injetável, para testes de TTL e de lease. */
  agora?: () => Date;
  ttlMs?: number;
  /** Timeout da tool; o lease vira timeout + margem, salvo `leaseMs`. */
  timeoutMs?: number;
  /** Só para testes de vencimento do lease; em produção derive com `leaseMsDeTimeout`. */
  leaseMs?: number;
};

export interface RepositorioAcoes {
  criar(acao: Omit<AcaoPendente, "expira_em"> & { expira_em?: string }): Promise<void>;
  /** Só devolve a ação do próprio usuário (o RLS faz o mesmo na leitura). */
  buscar(id: string, usuarioId: string): Promise<AcaoPendente | null>;
  /**
   * Troca `pendente` por `executando` de forma atômica. Devolve a ação se esta
   * chamada ganhou; `null` se não existe, é de outro usuário, já saiu de
   * `pendente`, expirou o TTL ou o lease de `executando` venceu (nesses dois
   * últimos casos a linha é marcada `expirada` ou `falhou` e auditada).
   */
  reivindicar(
    id: string,
    usuarioId: string,
    em: string,
    /** Timeout da tool nesta aprovação; o lease deriva daqui (fonte única). */
    timeoutMs?: number,
  ): Promise<AcaoPendente | null>;
  /**
   * Só aceita ação `pendente` ainda no prazo. Devolve a ação `rejeitada` ou
   * `null` (não encontrada, de outro usuário, já decidida ou expirada).
   */
  rejeitar(id: string, usuarioId: string, em: string): Promise<AcaoPendente | null>;
  concluir(id: string, desfecho: DesfechoAcao): Promise<AcaoPendente>;
  auditar(registro: RegistroAuditoria): Promise<void>;
  auditoria(acaoId: string): Promise<RegistroAuditoria[]>;
}

/** Implementação em memória, para testes e para o modelo falso em desenvolvimento. */
export function repositorioAcoesEmMemoria(opts: OpcoesRepositorioAcoes = {}): RepositorioAcoes {
  const acoes = new Map<string, AcaoPendente>();
  const registros: RegistroAuditoria[] = [];
  const agora = opts.agora ?? (() => new Date());
  const ttlMs = opts.ttlMs ?? ACAO_TTL_PADRAO_MS;
  const leaseAtual = (timeoutMs?: number): number =>
    opts.leaseMs ?? leaseMsDeTimeout(timeoutMs ?? opts.timeoutMs ?? timeoutAtualMs());
  const copia = (a: AcaoPendente): AcaoPendente => structuredClone(a);

  const doDono = (id: string, usuarioId: string): AcaoPendente | undefined => {
    const a = acoes.get(id);
    return a && a.usuario_id === usuarioId ? a : undefined;
  };

  const auditarSync = (registro: RegistroAuditoria) => {
    registros.push({ ...registro });
  };

  const expirarSeVencida = (a: AcaoPendente, em: string): boolean => {
    if (a.status !== "pendente") {
      return false;
    }
    if (Date.parse(a.expira_em) > Date.parse(em)) {
      return false;
    }
    a.status = "expirada";
    auditarSync({ acao_id: a.id, usuario_id: a.usuario_id, evento: "expirada", em });
    return true;
  };

  const encerrarLeaseVencido = (a: AcaoPendente, em: string, timeoutMs?: number): boolean => {
    if (a.status !== "executando" || !a.executando_em) {
      return false;
    }
    if (Date.parse(a.executando_em) + leaseAtual(timeoutMs) > Date.parse(em)) {
      return false;
    }
    a.status = "falhou";
    a.erro = "execução interrompida (timeout da reivindicação)";
    auditarSync({ acao_id: a.id, usuario_id: a.usuario_id, evento: "falhou", em });
    return true;
  };

  return {
    async criar(acao) {
      const expira_em = acao.expira_em ?? new Date(agora().getTime() + ttlMs).toISOString();
      const criada = copia({ ...acao, expira_em });
      acoes.set(criada.id, criada);
    },
    async buscar(id, usuarioId) {
      const a = doDono(id, usuarioId);
      return a ? copia(a) : null;
    },
    async reivindicar(id, usuarioId, _em, timeoutMs) {
      const em = agora().toISOString();
      const a = doDono(id, usuarioId);
      if (!a) {
        return null;
      }
      if (expirarSeVencida(a, em) || encerrarLeaseVencido(a, em, timeoutMs)) {
        return null;
      }
      if (a.status !== "pendente") {
        return null;
      }
      a.status = "executando";
      a.aprovado_por = usuarioId;
      a.aprovado_em = em;
      a.executando_em = em;
      auditarSync({ acao_id: a.id, usuario_id: usuarioId, evento: "aprovada", em });
      return copia(a);
    },
    async rejeitar(id, usuarioId) {
      const em = agora().toISOString();
      const a = doDono(id, usuarioId);
      if (!a) {
        return null;
      }
      if (expirarSeVencida(a, em) || encerrarLeaseVencido(a, em)) {
        return null;
      }
      if (a.status !== "pendente") {
        return null;
      }
      a.status = "rejeitada";
      auditarSync({ acao_id: a.id, usuario_id: usuarioId, evento: "rejeitada", em });
      return copia(a);
    },
    async concluir(id, desfecho) {
      const a = acoes.get(id);
      if (!a) {
        throw new Error(`ação ${id} não existe`);
      }
      if (a.status !== "executando") {
        throw new Error(`ação ${id} não está em executando`);
      }
      a.status = desfecho.status;
      if (desfecho.status === "executada") {
        a.resultado = desfecho.resultado;
      } else {
        a.erro = desfecho.erro;
      }
      auditarSync({
        acao_id: a.id,
        usuario_id: a.usuario_id,
        evento: desfecho.status,
        em: agora().toISOString(),
      });
      return copia(a);
    },
    async auditar(registro) {
      auditarSync(registro);
    },
    async auditoria(acaoId) {
      return registros.filter((r) => r.acao_id === acaoId).map((r) => ({ ...r }));
    },
  };
}

/**
 * O repositório padrão das rotas de aprovação/rejeição vive em
 * `acoes-padrao.ts` (`criarRepositorioPadrao`): Supabase com service_role
 * quando a chave existe; senão memória por processo (falha segura, 404).
 */
