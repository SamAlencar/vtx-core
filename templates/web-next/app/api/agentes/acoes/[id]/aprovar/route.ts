import { criarPostAprovar } from "@/src/agentes/rotas/aprovar";

// VTX-213: única porta de execução de tool crítica. Exige usuário autenticado.
export const POST = criarPostAprovar();
