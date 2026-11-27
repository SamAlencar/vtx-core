import type { ToolRegistro } from "@/src/agentes/harness";
import { definicaoSomar } from "./exemplo";

/** Tools que a rota de aprovação conhece. Só as com `critica: true` são aprovadas. */
export const catalogoTools: ToolRegistro[] = [definicaoSomar];
