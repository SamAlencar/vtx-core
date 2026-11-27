export type Limiares = {
  acerto_tool: number;
  validade_schema: number;
  recusa_correta: number;
  passos_medio_max: number;
};

export type Metricas = {
  acerto_tool: number;
  validade_schema: number;
  recusa_correta: number;
  passos_medio: number;
};

export type FalhaLimiar = { metrica: keyof Metricas | "passos_medio_max"; obtido: number; limiar: number };

export function avaliar(metricas: Metricas, limiares: Limiares): FalhaLimiar[] {
  const falhas: FalhaLimiar[] = [];
  for (const chave of ["acerto_tool", "validade_schema", "recusa_correta"] as const) {
    if (metricas[chave] + 1e-9 < limiares[chave]) {
      falhas.push({ metrica: chave, obtido: metricas[chave], limiar: limiares[chave] });
    }
  }
  if (metricas.passos_medio - 1e-9 > limiares.passos_medio_max) {
    falhas.push({
      metrica: "passos_medio_max",
      obtido: metricas.passos_medio,
      limiar: limiares.passos_medio_max,
    });
  }
  return falhas;
}
