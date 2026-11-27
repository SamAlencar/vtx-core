"use client";

import { useState, type FormEvent } from "react";
import {
  entradaAssistente,
  saidaAssistente,
  type SaidaAssistente,
} from "@/src/agentes/contrato";

type ErroVisivel = {
  title?: string;
  detail?: string;
  codigo?: string;
  trace_id?: string;
  status?: number;
};

export default function AssistentePage() {
  const [objetivo, setObjetivo] = useState("Some 1 e 2");
  const [resultado, setResultado] = useState<SaidaAssistente | null>(null);
  const [erro, setErro] = useState<ErroVisivel | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function enviar(ev: FormEvent) {
    ev.preventDefault();
    setErro(null);
    setResultado(null);
    const lido = entradaAssistente.safeParse({ objetivo });
    if (!lido.success) {
      setErro({ title: "Entrada inválida", detail: "Informe um objetivo.", status: 422 });
      return;
    }
    setEnviando(true);
    try {
      const res = await fetch("/api/agentes/exemplo", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(lido.data),
      });
      const corpo: unknown = await res.json();
      if (!res.ok) {
        setErro((corpo ?? {}) as ErroVisivel);
        return;
      }
      setResultado(saidaAssistente.parse(corpo));
    } catch {
      setErro({ title: "Falha de rede", detail: "Não foi possível falar com o agente." });
    } finally {
      setEnviando(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-6 p-8">
      <h1 className="text-3xl font-semibold">Assistente</h1>
      <p className="text-zinc-600">
        Exemplo de fluxo ponta a ponta: a tela chama a API, que usa o harness e a
        tool de domínio.
      </p>
      <form onSubmit={enviar} className="flex flex-col gap-3">
        <label htmlFor="objetivo" className="font-medium">
          Objetivo
        </label>
        <textarea
          id="objetivo"
          name="objetivo"
          rows={3}
          className="rounded border border-zinc-300 bg-white p-2"
          value={objetivo}
          onChange={(e) => setObjetivo(e.target.value)}
        />
        <button
          type="submit"
          disabled={enviando}
          className="w-fit rounded bg-zinc-900 px-4 py-2 text-white disabled:opacity-60"
        >
          {enviando ? "Enviando…" : "Enviar"}
        </button>
      </form>
      {erro ? (
        <div role="alert" className="rounded border border-red-200 bg-red-50 p-3 text-red-900">
          <p className="font-medium">{erro.title ?? "Erro"}</p>
          {erro.detail ? <p>{erro.detail}</p> : null}
          {erro.codigo ? <p>Código: {erro.codigo}</p> : null}
          {erro.trace_id ? <p>Trace: {erro.trace_id}</p> : null}
        </div>
      ) : null}
      {resultado ? (
        <section className="flex flex-col gap-2 rounded border border-zinc-200 bg-white p-4">
          <p data-testid="resposta-texto">{resultado.texto}</p>
          <p data-testid="trace-id">trace_id: {resultado.trace_id}</p>
          <p data-testid="tools-chamadas">
            tools: {resultado.toolsChamadas.join(", ") || "(nenhuma)"}
          </p>
          {resultado.dados ? (
            <p data-testid="dados-total">total: {resultado.dados.total}</p>
          ) : null}
        </section>
      ) : null}
    </main>
  );
}
