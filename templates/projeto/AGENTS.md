# AGENTS.md — __NOME_DO_PROJETO__

Repositório de cliente da VTX. Idioma: pt-BR. Trabalho vira artefato aqui; não fica só na conversa.

## Como começar

1. Identifique o papel e siga o SOP e a governança A0–A3 do núcleo VTX
   (`https://github.com/SamAlencar/vtx-core`, arquivos `AGENTS.md`,
   `knowledge/processos/fluxo-entre-agentes.md` e
   `knowledge/processos/governanca-e-aprovacoes.md`).
2. Artefatos deste repositório: [PRD](docs/produto/PRD.md), [arquitetura](docs/arquitetura.md),
   [ADRs](docs/adr/0000-modelo.md), [plano](docs/plano.md), [testes](testes/plano.md) e
   [runbook](docs/runbook.md).
3. Regras do Cursor em [`.cursor/rules/`](.cursor/rules/). Memory bank em `docs/memoria/` e
   mapa de codebase em `docs/CODEBASE_MAP.md` (crie quando o código existir); leitura sob demanda.

## Conduta

- Sem segredo ou dado pessoal em prompt, commit ou chat. Use `.env` (veja [`.env.example`](.env.example)).
- Sem produção e sem serviço pago sem aprovação do Samuel (A2).
- Quem produz não aprova o próprio trabalho. PR com testes e CI verde.
