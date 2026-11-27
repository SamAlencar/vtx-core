/** Corpo de erro no formato RFC 9457 (Problem Details). */
export type ProblemDetails = {
  type: string;
  title: string;
  status: number;
  detail?: string;
  instance?: string;
};

export function problema(
  status: number,
  title: string,
  detail?: string,
  type = "about:blank",
): ProblemDetails {
  const corpo: ProblemDetails = { type, title, status };
  if (detail) {
    corpo.detail = detail;
  }
  return corpo;
}
