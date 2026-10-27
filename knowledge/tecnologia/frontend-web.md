# Desenvolvimento frontend web

> VTX-026 · Fase F4 · Base de Conhecimento. Como o **Dev Frontend/Mobile** ([dev-frontend-mobile.md](../../agents/dev-frontend-mobile.md)) constrói telas web sobre o [stack de referência](stack-de-referencia.md) (Next.js App Router + React + Tailwind + shadcn/ui). Contratos: [design de APIs](design-de-apis.md). App: [mobile](mobile.md).

## 1. Conceitos
- **Server Components por padrão:** a página busca dados no servidor e manda HTML pronto; `"use client"` só no pedaço que precisa de estado, evento ou API do navegador. Menos JavaScript no celular do usuário.
- **Fronteira de segredo:** só variáveis `NEXT_PUBLIC_*` vão para o navegador, e nelas só vai o que é público (URL e chave `anon` do Supabase). `service_role`, chaves do Stripe e tokens ficam no servidor (Route Handler, Server Action, Edge Function).
- **Core Web Vitals (metas do Google, percentil 75):** LCP ≤ 2,5 s (carregamento), INP ≤ 200 ms (resposta ao toque), CLS ≤ 0,1 (estabilidade). Medir em celular com 4G, não no notebook do Dev.
- **Acessibilidade WCAG 2.2 nível AA:** contraste mínimo de 4,5:1, tudo operável pelo teclado com foco visível, rótulo em todo campo, alvo de toque de pelo menos 24×24 px, idioma `pt-BR` no `<html>`. Detalhes e checklist em [UX/UI e acessibilidade](ux-ui-acessibilidade.md).
- **Princípios de UX** ([UX](../design/principios-de-ux.md)): uma ação principal por tela (Hick), formulários em etapas curtas (Miller), padrões conhecidos (Jakob), CEP preenche o endereço (Tesler), máscara opcional e normalização no servidor (Postel).

## 2. Metodologia (por tela)
1. **Partir do Figma e da história:** estados obrigatórios: carregando (skeleton), vazio (com próxima ação), erro (mensagem legível e "tentar de novo") e sucesso. Sem design para um estado → perguntar ao Produto, não inventar.
2. **Montar com o design system:** componentes shadcn/ui e tokens do Tailwind vindos do Figma; nada de cor ou espaçamento "solto". Componente novo só se não houver equivalente.
3. **Dados sem cascata** (skill `react-best-practices`, prioridade crítica): buscas independentes em paralelo (`Promise.all`), `Suspense` para transmitir o que já está pronto, cache por requisição com `React.cache`.
4. **Bundle enxuto:** importar direto (sem arquivos "barril"), `next/dynamic` para mapa, editor, visualizador 3D/IFC; `next/image` e `next/font`; scripts de terceiros depois da hidratação.
5. **Formulários:** mesmo schema Zod do contrato no cliente (aviso imediato) e no servidor (validação real); nunca perder o que foi digitado ao dar erro; botão desabilitado durante o envio (evita POST duplo, que a API trata com `Idempotency-Key`).
6. **Autorização:** a tela só esconde o que o usuário não pode ver; quem decide é a RLS/servidor. Server Action se autentica como uma rota de API.
7. **Testar:** Vitest + Testing Library nos componentes com regra; Playwright no fluxo principal com `@axe-core/playwright` (zero violação séria) ([testes](../engenharia/testes-e-qualidade.md)); Lighthouse no preview da Vercel.

## 3. Exemplo: página de projetos
```tsx
// app/projetos/page.tsx (Server Component)
export default async function Page() {
  const supabase = await criarClienteServidor(); // sessão do usuário; RLS filtra
  const [{ data: projetos }, perfil] = await Promise.all([
    supabase.from("projetos").select("id, nome, status").limit(20),
    buscarPerfil(),
  ]);
  if (!projetos?.length) return <Vazio acao="Criar primeiro projeto" />;
  return <ListaProjetos itens={projetos} perfil={perfil} />; // só a busca é "use client"
}
```

## 4. Checklist do PR de frontend
- [ ] Os 4 estados (carregando, vazio, erro, sucesso) existem e foram vistos no preview.
- [ ] Nenhum segredo em `NEXT_PUBLIC_*` nem em componente cliente.
- [ ] Sem cascata de `await`; componentes pesados com `next/dynamic`.
- [ ] LCP ≤ 2,5 s, INP ≤ 200 ms e CLS ≤ 0,1 no Lighthouse mobile do preview.
- [ ] axe sem violação séria; navegação só por teclado testada; contraste AA.
- [ ] Formulário valida com o schema Zod do contrato e não perde dados no erro.
- [ ] Textos em pt-BR claros; uma ação principal por tela.

## 5. Fontes
- Next.js — Server e Client Components: https://nextjs.org/docs/app/getting-started/server-and-client-components
- Next.js — variáveis de ambiente: https://nextjs.org/docs/app/guides/environment-variables
- Web Vitals (Google): https://web.dev/articles/vitals
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- React — Suspense: https://react.dev/reference/react/Suspense
- Vercel React Best Practices: https://github.com/vercel-labs/agent-skills
- shadcn/ui: https://ui.shadcn.com/docs
- axe-core Playwright: https://playwright.dev/docs/accessibility-testing
