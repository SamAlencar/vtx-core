/** Corpo de erro no formato RFC 9457 (Problem Details). */
export type ProblemDetails = {
  type: string;
  title: string;
  status: number;
  detail?: string;
  instance?: string;
  codigo?: string;
  trace_id?: string;
};

export function problema(
  status: number,
  title: string,
  detail?: string,
  type = "about:blank",
  extra?: { codigo?: string; trace_id?: string },
): ProblemDetails {
  const corpo: ProblemDetails = { type, title, status };
  if (detail) {
    corpo.detail = detail;
  }
  if (extra?.codigo) {
    corpo.codigo = extra.codigo;
  }
  if (extra?.trace_id) {
    corpo.trace_id = extra.trace_id;
  }
  return corpo;
}
