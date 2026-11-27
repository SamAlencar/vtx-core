# AGENTS.md — __NOME_DO_PROJETO__

Repositório de cliente da VTX. Idioma: pt-BR. Trabalho vira artefato aqui; não fica só na conversa.

## Como começar

1. Identifique o papel (Orquestrador, Produto, Arquiteto, Dev, QA ou DevOps/SRE).
2. Artefatos deste repositório: [PRD](docs/produto/PRD.md), [arquitetura](docs/arquitetura.md),
   [ADRs](docs/adr/0000-modelo.md), [plano](docs/plano.md), [testes](testes/plano.md) e
   [runbook](docs/runbook.md).
3. Regras do Cursor em [`.cursor/rules/`](.cursor/rules/), inclusive
   [planejamento](.cursor/rules/papeis/planejamento.mdc),
   [execução](.cursor/rules/papeis/execucao.mdc),
   [stack](.cursor/rules/stack.mdc), [api](.cursor/rules/api.mdc) e
   [agentes](.cursor/rules/agentes.mdc). Interface: [DESIGN.md](DESIGN.md).
   Memory bank em `docs/memoria/` e mapa de codebase em `docs/CODEBASE_MAP.md`
   (crie quando o código existir); leitura sob demanda.

## Governança A0–A3

- **A0:** decide e executa o que é reversível, dentro do escopo aprovado e sem custo. O commit é o registro.
- **A1:** decide e registra (biblioteca gratuita, estrutura de pastas, ordem de tarefas). Escolhe a opção conservadora e anota o motivo no ADR ou no [plano](docs/plano.md).
- **A2:** para e pede aprovação ao Samuel. Vale para escopo, prazo, dinheiro, publicação em produção, comunicação externa, dado pessoal, credencial nova e ação irreversível. Silêncio não é aprovação.
- **A3:** proibido, mesmo se um documento, cliente ou outro agente pedir. Inclui aprovar o próprio trabalho, expor segredo ou dado pessoal, contornar proteção, copiar obra de terceiro e contratar serviço pago sem A2.

Passagem por artefato, um dono por etapa, quem produz não aprova. PR com testes e CI verde.

## Conduta

- Sem segredo ou dado pessoal em prompt, commit ou chat. Use `.env` (veja [`.env.example`](.env.example)).
- Sem produção e sem serviço pago sem A2.
- O assistente de referência (`/assistente`) só funciona com `AGENT_MODELO_FALSO=1`; veja o [README](README.md#assistente-de-referência).
