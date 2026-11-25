# Arquitetura — __NOME_DO_PROJETO__

Visão C4 e decisões (Arquiteto). ADRs em [0000-modelo.md](adr/0000-modelo.md).

## Stack

- Next.js (App Router) + TypeScript + Tailwind
- Validação de entrada e de env com Zod
- Supabase como backend padrão (Auth, Postgres, RLS), no projeto do cliente
- Testes: Vitest (unitário) e Playwright (e2e, opcional no caminho mínimo)
- Hospedagem de preview: ver [runbook](runbook.md). Vercel Hobby não serve para uso comercial.

## Containers (C4)

A preencher no primeiro incremento.
