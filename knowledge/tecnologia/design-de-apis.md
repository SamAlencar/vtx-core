# Design de APIs

> VTX-024 · Fase F4 · Base de Conhecimento. Como o **Arquiteto** define e o **Dev Backend** ([dev-backend.md](../../agents/dev-backend.md)) implementa APIs nos projetos da VTX, sobre o [stack de referência](stack-de-referencia.md). Banco e RLS: [modelagem de dados](modelagem-de-dados.md).

## 1. Conceitos
- **Contrato primeiro (contract-first):** o contrato (OpenAPI 3.1 ou schemas Zod que geram o OpenAPI) é escrito e revisado antes do código; front, mobile e QA trabalham em paralelo contra ele.
- **Qual estilo usar:** (a) dados simples do próprio app → `supabase-js` direto, protegido por RLS, sem API própria; (b) regra de negócio, integração ou segredo → Route Handler do Next.js (`app/api/.../route.ts`) ou Edge Function; (c) evento externo → webhook. GraphQL/gRPC só com ADR.
- **REST com semântica HTTP (RFC 9110):** recursos no plural (`/projetos/{id}/arquivos`), verbos pelo método (GET lê, POST cria, PATCH altera parte, DELETE remove), GET/PUT/DELETE **idempotentes**.
- **Erros padronizados (RFC 9457, Problem Details):** `application/problem+json` com `type`, `title`, `status`, `detail` e `errors[]` por campo; nunca stack trace nem SQL na resposta.
- **Idempotência:** POST que cobra, envia ou cria aceita `Idempotency-Key`; webhooks guardam o id do evento (como o Stripe em [pagamentos](../engenharia/pagamentos.md)).

## 2. Metodologia (por endpoint)
1. **Partir da história de usuário:** quem chama, com que permissão, quais dados (pessoal? LGPD) e o critério de aceite negativo (acesso negado), como em [desenvolvimento seguro](../seguranca/desenvolvimento-seguro.md).
2. **Escrever o contrato:** caminho, método, schema Zod de entrada e saída, códigos de status, exemplo de requisição/resposta. Revisão do Arquiteto antes de codar.
3. **Validar na borda com Zod** e ser tolerante no que é inofensivo (lei de Postel, ver [UX](../design/principios-de-ux.md)): `trim`, e-mail em minúsculas, CPF/CEP com ou sem máscara, datas ISO 8601. Rejeitar o resto com 422 e mensagem legível.
4. **Autorizar no servidor:** sessão Supabase (JWT) → usuário → checar dono/papel; o cliente nunca decide permissão. `service_role` só no servidor.
5. **Responder de forma previsível:** JSON `camelCase`, datas ISO 8601 em UTC, dinheiro em centavos inteiros + moeda, listas paginadas por cursor (`?limite=20&cursor=...` → `{ itens, proximoCursor }`), limite máximo fixo.
6. **Proteger:** rate limit nas rotas públicas e de login (Vercel Firewall/WAF do plano gratuito ou contador no Postgres), CORS só para os domínios do projeto, tamanho máximo de corpo.
7. **Testar:** teste de contrato (schema Zod de saída valida a resposta), caso feliz, 401/403, 422 e repetição idempotente no Vitest ([testes](../engenharia/testes-e-qualidade.md)).
8. **Documentar e versionar:** OpenAPI gerado do Zod no repositório; mudança só **aditiva** (campo novo opcional). Quebra → `/v2` ou novo campo, com prazo de desativação, pois apps mobile antigos continuam chamando.

### Códigos de status usados
| Código | Quando |
|---|---|
| 200 / 201 / 204 | leu ou alterou / criou (com `Location`) / removeu sem corpo |
| 400 / 422 | corpo malformado / falhou na validação de campos |
| 401 / 403 / 404 | sem sessão / sem permissão / não existe (ou não pode saber que existe) |
| 409 / 429 | conflito de estado ou chave repetida / limite de requisições |
| 500 | erro inesperado: logado com `trace_id` ([observabilidade](../operacao/observabilidade.md)), resposta genérica |

## 3. Exemplo
```ts
// app/api/projetos/route.ts — POST /api/projetos
const Entrada = z.object({ nome: z.string().trim().min(3).max(120), cidade: z.string().trim() });
export async function POST(req: Request) {
  const usuario = await usuarioDaSessao(req);            // 401 se não houver
  const r = Entrada.safeParse(await req.json());
  if (!r.success) return problema(422, "Dados inválidos", r.error.flatten().fieldErrors);
  const projeto = await criarProjeto(usuario.id, r.data, req.headers.get("Idempotency-Key"));
  return Response.json(projeto, { status: 201, headers: { Location: `/api/projetos/${projeto.id}` } });
}
```

## 4. Checklist do PR de API
- [ ] Contrato (Zod/OpenAPI) revisado antes do código; exemplo de requisição e resposta.
- [ ] Entrada validada com Zod; variações inofensivas aceitas; 422 com erros por campo.
- [ ] Autorização no servidor; teste de usuário A tentando acessar dado de B (403/404).
- [ ] Erros em Problem Details, sem stack trace; 500 logado com `trace_id`.
- [ ] POST sensível idempotente; listas paginadas com limite máximo.
- [ ] Nenhuma quebra de contrato (ou versão nova com prazo); OpenAPI atualizado.
- [ ] Sem segredo no código; rate limit e CORS nas rotas públicas.

## 5. Fontes
- RFC 9110 — HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110
- RFC 9457 — Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457
- OpenAPI Specification 3.1: https://spec.openapis.org/oas/v3.1.0
- Microsoft REST API Guidelines: https://github.com/microsoft/api-guidelines
- Zod: https://zod.dev/
- Next.js Route Handlers: https://nextjs.org/docs/app/building-your-application/routing/route-handlers
- OWASP API Security Top 10 (2023): https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- Stripe — requisições idempotentes: https://docs.stripe.com/api/idempotent_requests
