import type { SupabaseClient } from "@supabase/supabase-js";
import {
  ACAO_TTL_PADRAO_MS,
  leaseMsDeTimeout,
  type AcaoPendente,
  type DesfechoAcao,
  type OpcoesRepositorioAcoes,
  type RegistroAuditoria,
  type RepositorioAcoes,
  type StatusAcao,
} from "./acoes";

type LinhaAcao = {
  id: string;
  usuario_id: string;
  tool: string;
  input: unknown;
  status: StatusAcao;
  trace_id: string;
  criado_em: string;
  expira_em: string;
  executando_em?: string | null;
  contexto_retomada?: AcaoPendente["contexto_retomada"] | null;
  aprovado_por?: string | null;
  aprovado_em?: string | null;
  resultado?: unknown;
  erro?: string | null;
};

function deLinha(a: LinhaAcao): AcaoPendente {
  return {
    id: a.id,
    usuario_id: a.usuario_id,
    tool: a.tool,
    input: a.input,
    status: a.status,
    trace_id: a.trace_id,
    criado_em: a.criado_em,
    expira_em: a.expira_em,
    ...(a.executando_em ? { executando_em: a.executando_em } : {}),
    ...(a.contexto_retomada ? { contexto_retomada: a.contexto_retomada } : {}),
    ...(a.aprovado_por ? { aprovado_por: a.aprovado_por } : {}),
    ...(a.aprovado_em ? { aprovado_em: a.aprovado_em } : {}),
    ...(a.resultado !== undefined && a.resultado !== null
      ? { resultado: a.resultado }
      : {}),
    ...(a.erro ? { erro: a.erro } : {}),
  };
}

function intervaloLease(ms: number): string {
  const seg = Math.max(1, Math.ceil(ms / 1000));
  return `${seg} seconds`;
}

function timeoutAtualMs(): number {
  const bruto = Number(process.env.AGENT_TIMEOUT_MS);
  return Number.isFinite(bruto) && bruto > 0 ? bruto : 30_000;
}

/**
 * Repositório Supabase: escrita só via service_role / RPC security definer.
 * Nunca usa o JWT do usuário para insert/update/delete.
 *
 * As RPCs já auditam criar/reivindicar/concluir/rejeitar. O harness ainda
 * chama `auditar({ evento: "criada" })` depois de `criar` (contrato da
 * implementação em memória, que não audita no `criar`). Neste repositório
 * `auditar` é no-op para não duplicar a trilha.
 *
 * `buscar` lê pelo service_role, inclusive `contexto_retomada` (necessário
 * na retomada). Filtra pelo dono no código. A leitura do usuário autenticado
 * continua sendo GRANT SELECT por coluna / view `acoes_pendentes_leitura`
 * (sem `contexto_retomada`), como na migração da VTX-213.
 */
export function repositorioAcoesSupabase(
  cliente: SupabaseClient,
  opts: OpcoesRepositorioAcoes = {},
): RepositorioAcoes {
  const agora = opts.agora ?? (() => new Date());
  const ttlMs = opts.ttlMs ?? ACAO_TTL_PADRAO_MS;
  const leaseAtual = (timeoutMs?: number): number =>
    opts.leaseMs ??
    leaseMsDeTimeout(timeoutMs ?? opts.timeoutMs ?? timeoutAtualMs());

  return {
    async criar(acao) {
      const em = agora().toISOString();
      const expira_em =
        acao.expira_em ?? new Date(agora().getTime() + ttlMs).toISOString();
      const { error } = await cliente.rpc("acoes_criar", {
        p_id: acao.id,
        p_usuario_id: acao.usuario_id,
        p_tool: acao.tool,
        p_input: acao.input,
        p_trace_id: acao.trace_id,
        p_em: em,
        p_expira_em: expira_em,
        p_contexto_retomada: acao.contexto_retomada ?? null,
      });
      if (error) {
        throw new Error(`acoes_criar: ${error.message}`);
      }
    },

    async buscar(id, usuarioId) {
      const { data, error } = await cliente
        .from("acoes_pendentes")
        .select(
          "id, usuario_id, tool, input, status, trace_id, criado_em, expira_em, executando_em, contexto_retomada, aprovado_por, aprovado_em, resultado, erro",
        )
        .eq("id", id)
        .eq("usuario_id", usuarioId)
        .maybeSingle();
      if (error) {
        throw new Error(`buscar ação: ${error.message}`);
      }
      return data ? deLinha(data as LinhaAcao) : null;
    },

    async reivindicar(id, usuarioId, _em, timeoutMs) {
      const em = agora().toISOString();
      const { data, error } = await cliente.rpc("acoes_reivindicar", {
        p_id: id,
        p_usuario_id: usuarioId,
        p_em: em,
        p_lease: intervaloLease(leaseAtual(timeoutMs)),
      });
      if (error) {
        throw new Error(`acoes_reivindicar: ${error.message}`);
      }
      if (!data) {
        return null;
      }
      return deLinha(data as LinhaAcao);
    },

    async rejeitar(id, usuarioId) {
      const em = agora().toISOString();
      const { data, error } = await cliente.rpc("acoes_rejeitar", {
        p_id: id,
        p_usuario_id: usuarioId,
        p_em: em,
      });
      if (error) {
        throw new Error(`acoes_rejeitar: ${error.message}`);
      }
      if (!data) {
        return null;
      }
      return deLinha(data as LinhaAcao);
    },

    async concluir(id, desfecho: DesfechoAcao) {
      const { data, error } = await cliente.rpc("acoes_concluir", {
        p_id: id,
        p_status: desfecho.status,
        p_resultado:
          desfecho.status === "executada" ? desfecho.resultado ?? null : null,
        p_erro: desfecho.status === "falhou" ? desfecho.erro : null,
      });
      if (error) {
        throw new Error(`acoes_concluir: ${error.message}`);
      }
      if (!data) {
        throw new Error(`ação ${id} não está em executando`);
      }
      return deLinha(data as LinhaAcao);
    },

    async auditar() {
      // No-op de propósito: ver o comentário do módulo.
    },

    async auditoria(acaoId) {
      const { data, error } = await cliente
        .from("acoes_auditoria")
        .select("acao_id, usuario_id, evento, em")
        .eq("acao_id", acaoId)
        .order("em", { ascending: true });
      if (error) {
        throw new Error(`auditoria: ${error.message}`);
      }
      return (data ?? []).map((r) => ({
        acao_id: r.acao_id as string,
        usuario_id: r.usuario_id as string,
        evento: r.evento as RegistroAuditoria["evento"],
        em: r.em as string,
      }));
    },
  };
}
