# ADR-001: Refazer a plataforma do zero
- **Status:** aceito (decisão do Samuel em 18/10/2026, [etapa 5](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/etapa5-reaproveitar-ou-refazer.md))
- **Data:** 20/10/2026 · **Nível de governança:** A2 (aprovado)

## Contexto
O repositório `SamAlencar/4medco-platform` (React, Vite, Supabase, Stripe, Stream, Gemini/OpenAI) tem cerca de 207 migrations caóticas, nenhum teste relevante, documentação contraditória e uma camada de IA e atendimento superdimensionada que não combina com o novo desenho chat-first ([raio X](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/raio-x-repositorios.md)). Ele também tem dois riscos de segurança (ver "Lição aprendida").

## Decisão
Criar um projeto novo, com schema único, limpo e testado. **Nenhum código é copiado.** O repositório antigo e o `4medco-website` servem só como referência de comportamento: o desenho das tabelas contábeis, as telas do contador e a regra do Fator R. Os dois repositórios antigos não serão alterados.

## Alternativas consideradas
- **A. Reaproveitar e limpar:** recusada. Herda os riscos de segurança e a dívida técnica, e não encaixa no chat com MCPs.
- **C. Híbrida (copiar partes escolhidas):** era a recomendação técnica, mas foi recusada pelo Samuel. Copiar arquivos traz dependências ruins.

## Consequências
- (+) Segurança limpa desde o início; RLS com 3 perfis (médico, parceiro, admin).
- (+) Encaixa no fluxo VTX `sistema-web-saas` como projeto novo.
- (−) Refazer telas contábeis que já funcionavam: esforço G. Para reduzir, use o [inventário da etapa 5](https://github.com/SamAlencar/4medco-base-conhecimento/blob/0da4cba/etapa5-reaproveitar-ou-refazer.md#3-inventário-do-que-vale-levar-repo-samalencar4medco-platform) como especificação de referência.
- O site também será refeito, como projeto separado no fluxo `site-landing-page`.

## Lição aprendida: dois riscos do repositório antigo
Estes erros **não podem se repetir** no projeto novo. Eles viram os NFR-05 e NFR-06 do [PRD](../produto/PRD.md#6-requisitos-não-funcionais-iso-iec-25010).
1. **Chave service role lida por variável `VITE_`.** O código antigo lia `VITE_SUPABASE_SERVICE_ROLE_KEY`. Toda variável `VITE_` vai para o JavaScript do navegador, e essa chave ignora a RLS: quem a obtém lê e altera o banco inteiro. **Regra:** só a chave `anon`/publishable no front-end; a service role fica apenas no servidor (Edge Functions, MCP da plataforma) e o CI tem varredura de segredos (gitleaks).
2. **Função `exec_sql` liberada a usuários autenticados.** Uma função que executa SQL arbitrário, com `GRANT` para `authenticated`, deixa qualquer usuário logado rodar qualquer comando. **Regra:** nunca criar função de SQL dinâmico exposta; funções com `SECURITY INVOKER` por padrão; `SECURITY DEFINER` só com revisão de Segurança e `search_path` fixo; rodar o Security Advisor do Supabase no CI.
Situação atual: decisão do Samuel de 18/10/2026 de deixar como está enquanto a plataforma antiga está parada e sem clientes. Ao reativar qualquer ambiente antigo, revogar `exec_sql` e trocar a chave service role.

Fontes: Vite, *Env Variables and Modes* (https://vite.dev/guide/env-and-mode) · Supabase, *API keys* (https://supabase.com/docs/guides/api/api-keys) · Supabase, *Database functions / security* (https://supabase.com/docs/guides/database/functions). Consultadas em 20/10/2026.
