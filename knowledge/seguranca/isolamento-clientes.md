# Isolamento por cliente

> Segurança · Adotada (A1) · Revisado em 2026-11-24
> VTX-175 (auditoria 24/11/2026, P1 item 11). Complementa [desenvolvimento seguro](desenvolvimento-seguro.md) e o [template de repositório de cliente](../templates/projeto.md).

## ADR: um repositório por cliente

- **Status:** aceito (A1, estrutura de pastas e escopo de acesso).
- **Data:** 24/11/2026.

### Contexto

Até aqui, PRD, ADRs e notas de mais de um cliente/produto conviviam em `projects/` no vtx-core, o mesmo repositório que todos os agentes leem. Não havia regra que impedisse um agente de carregar o contexto de um cliente no trabalho de outro, nem de misturar segredos. O [template de projeto](../templates/projeto.md) (VTX-170) já gera um repositório separado; faltava a política.

### Decisão

Cada cliente ou produto entregue a cliente tem **um repositório próprio**, criado por `scripts/bootstrap_projeto.sh`. O vtx-core guarda só **ponteiro e metadados públicos** (nome, link, status). Código, dados, `.env` e secrets do GitHub ficam no repositório do cliente. Um agente trabalha em um repositório de cliente de cada vez e não carrega artefatos de outro cliente.

### Alternativas consideradas

- **Monorepo no vtx-core:** recusada. Facilita o painel, mas quebra o isolamento e amplia o blast radius de um vazamento de contexto ou de segredo.
- **Um repositório por cliente, com o core espelhando o código:** recusada. Duplica a superfície e anula a separação.

### Consequências

- (+) Segredos e PII não entram no vtx-core. O acesso segue o repositório em que a tarefa roda.
- (+) O template e o bootstrap (VTX-170) são o caminho padrão de projeto novo.
- (−) `projects/med-hub/` e `projects/plataforma-projetos/` ainda têm documentação no core (legado). A migração está na VTX-187. Não se adiciona código nem dado operacional nessas pastas.
- Sandboxes de ferramenta da VTX (`projects/sandbox-*`) não são repositório de cliente; continuam no core, sem dado de cliente.

## 2. O que pode ficar em `projects/` no vtx-core

| Tipo | Pode | Não pode |
|---|---|---|
| Ponteiro de cliente | `README.md` com o link do repositório, `conexoes.yaml` e metadados públicos | código-fonte, `.env`, banco, dump, PII, segredo |
| Legado (`med-hub`, `plataforma-projetos`) | documentação já versionada, até a migração | código-fonte, segredo ou dado operacional novo |
| Sandbox de ferramenta (`sandbox-*`) | script e exemplo do piloto, sem PII de cliente | copiar PRD, base ou segredo de cliente |

## 3. Segredos

Segredo de cliente (token, chave, `.env`) vive nos *GitHub Secrets* e no `.env` local do **repositório dele**, nunca no vtx-core. `.env` não se commita; o modelo é o `.env.example` do template. Expor segredo ou dado pessoal em prompt, commit ou chat continua A3.

## 4. Permissões dos papéis

O escopo é o repositório da tarefa: no vtx-core, conhecimento e ponteiros; no repositório do cliente, só aquele projeto. Nenhum papel tem "leitura em todo o repositório" como licença para abrir outro cliente. DevOps/SRE acessa produção e secrets só do repositório em que opera, com mínimo privilégio.

## 5. Checklist (agente)

- [ ] Projeto novo de cliente sai do template, em repositório próprio — não em `projects/<cliente>/` no core.
- [ ] No vtx-core, `projects/<cliente>/` só tem ponteiro e metadados públicos (legado de docs: não acrescentar código nem dado).
- [ ] Segredo fica no repositório do cliente. Não copiar `.env` nem base para o core.
- [ ] Não carregar PRD, código ou dado de um cliente no contexto de outro.

## Fontes

- Auditoria 24/11/2026, parecer-vtx-core.md, P1 item 11.
- [Governança A0–A3](../processos/governanca-e-aprovacoes.md) · [Desenvolvimento seguro](desenvolvimento-seguro.md).
