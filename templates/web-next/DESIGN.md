# DESIGN.md — __NOME_DO_PROJETO__

Tokens, componentes e tom da interface deste repositório. A regra de stack aponta para cá.

## Tokens

Use as classes do Tailwind (`tailwind.config.ts`, `app/globals.css`). Não invente uma paleta paralela.

| Token | Uso | Classe de referência |
|---|---|---|
| Fundo | Página | `bg-white` (escuro: `dark:bg-zinc-950` quando houver tema) |
| Texto | Título e corpo | `text-zinc-900`, corpo auxiliar `text-zinc-600` |
| Destaque | Ação primária | `bg-zinc-900 text-white` |
| Espaço | Página | `p-8`, largura `max-w-2xl mx-auto`, fôlego `gap-4` |
| Tipo | Título | `text-3xl font-semibold`; corpo no tamanho padrão do template |

## Componentes

A interface começa em `app/`. Extraia um componente só quando ele se repetir. Prefira HTML semântico (`main`, `h1`, `p`, `button`) e classes Tailwind. Formato de erro visível ao usuário: mensagem curta; o detalhe técnico (RFC 9457) fica na API, não no texto da tela.

## Tom

Português do Brasil, direto e sóbrio. Sem jargão interno da VTX na interface do cliente. Frases curtas, verbos no infinitivo ou no presente. Sem emoji como ornamento. O nome do produto é o do repositório; não use "template" na tela depois da primeira entrega.
