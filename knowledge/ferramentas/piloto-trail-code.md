# Piloto local do Trail-code (graft map)

> Ferramentas · Adotado com restrições · Revisado em 2026-11-24
> VTX-135. Pin [trailhq/Trail-Code@b1211ef](https://github.com/trailhq/Trail-Code/tree/b1211ef), licença MIT.
> Sandbox: [projects/sandbox-trail-code/](../../projects/sandbox-trail-code/).

## 1. O que foi testado

Mapa de código local do Trail-code (árvore tree-sitter, sem rede e sem modelo) como ferramenta do [mapa de codebase](../engenharia/mapa-de-codebase.md). Instalação só no sandbox, sem `-g` e sem tocar na raiz do vtx-core. No pin o pacote npm é `@nanonets/graft@0.23.1` e o binário é `graft`, não `trail`.

Comandos permitidos: `graft build` (sem `--deep`), `ask`, `skeleton` e `check`. Proibidos: `graft init` (lê transcrições e PRs e envia à Anthropic), `build --deep` (LLM pago), conectar Trail workspace e ligar o MCP no vtx-core.

## 2. Como rodou

Em 24/11/2026, o script [`projects/sandbox-trail-code/scripts/rodar-piloto.sh`](../../projects/sandbox-trail-code/scripts/rodar-piloto.sh):

- exportou `DO_NOT_TRACK=1` antes do `npm install` e isolou `HOME` e o cache npm em `.home/` e `.npm-cache/` (gitignorados);
- instalou a árvore do `package-lock.json` com `npm ci --ignore-scripts` (o postinstall não roda, qualquer que seja a versão do npm);
- rodou `graft telemetry disable` e conferiu o status;
- copiou o vtx-core para `tmp-repo/` (gitignorado) e rodou o mapa contra essa cópia, não contra o worktree de trabalho;
- não criou `.trail/` (init não rodou).

Repetir: `projects/sandbox-trail-code/scripts/rodar-piloto.sh`. Não rodar `graft upgrade`.

## 3. Resultados (medidos)

| Medida | Valor |
|---|---|
| Versão | 0.23.1 |
| `graft build` (sem `--deep`) | ~1 s (`exemplos/tempo-build.txt` e `exemplos/build-resumo.txt`) |
| Grafo | 21 arquivos Python, 130 nós, 249 arestas (wiring), no commit `3327caa`; ver `exemplos/build-resumo.txt` |
| `skeleton` de `scripts/backlog_lib.py` | 107 tokens aproximados vs 391 do arquivo (~27%) |
| `graft ask "como o backlog escolhe a próxima tarefa"` | busca lexical, sem LLM: acertou `proxima_tarefa.py`, `backlog_lib.py` / `carregar`, `validar_backlog.py` (amostra em `exemplos/ask-proxima-tarefa-amostra.txt`) |
| `graft check` | wiring OK; o CLI sugere `--deep` — não foi rodado |
| `graft stats` | no pin o comando é `stats` (não `status`) |
| `.trail/` | não apareceu |

O build desta corrida (commit `3327caa`, rebaseado sobre a `main` com os PRs #21 e #22) indexou 21 de 26 arquivos Python versionados; os 5 que faltam estão em `.cursor/skills/ifc-python/`, que o graft não indexa. Markdown, YAML e shell também ficaram de fora do grafo. A evidência versionada está em `exemplos/build-resumo.txt`, com o SHA da corrida. Os números mudam quando o repositório ganha ou perde `.py` — por isso o resumo registra o commit, e o teste não trava a contagem. Não houve A/B de chamadas ou tokens de um agente com e sem o mapa: isso exigiria um segundo agente e não seria um número honesto aqui. O número do autor (−46% chamadas, −42% tokens) não foi reproduzido. O que deu para medir é a razão do `skeleton` (~27% dos tokens aproximados do arquivo).

A saída da ferramenta no `skeleton` chegou a citar economia maior; o que entra no registro é a medição acima (caracteres / 4).

## 4. Decisão

**Adotado com restrições**, só como ferramenta local do mapa de codebase:

- Pode: `graft build` / `ask` / `skeleton` / `check` no sandbox, com `DO_NOT_TRACK=1`, `HOME` isolado e pin `0.23.1`.
- Não pode: `init`, `build --deep`, Trail workspace, `graft upgrade` para fora do pin, instalar na raiz do vtx-core ou com `-g`, versionar o grafo gerado (`tmp-repo/graft/` continua gitignorado). O Markdown do mapa de codebase continua sendo a fonte que se commita.
- O MCP do Trail-code **não** entra no vtx-core nesta etapa.
- O modelo decisão / preferência / guardrail em `.trail/` não foi exercitado (depende de `init`) e segue como insumo da VTX-132, se um dia for extraído sem `init`.

## 5. Checklist (agente)

- [ ] Instalar só em `projects/sandbox-trail-code/`, com `DO_NOT_TRACK=1` antes do npm.
- [ ] Usar o binário `graft` do pin `0.23.1`. Não rodar `init`, `build --deep`, `upgrade` nem conectar workspace.
- [ ] Não ligar o MCP no Cursor deste repositório.
- [ ] Instalar com `npm ci --ignore-scripts` a partir do `package-lock.json` versionado.
- [ ] Não commitar `node_modules/`, `.home/`, `.npm-cache/`, `.trail/`, `tmp-repo/` nem a saída bruta.

## Fontes

- Repositório e pin: [trailhq/Trail-Code@b1211ef](https://github.com/trailhq/Trail-Code/tree/b1211ef), MIT, consultados para o piloto em 24/11/2026.
- Medidas: `projects/sandbox-trail-code/exemplos/`.
- Registro: [`recursos.yaml`](recursos.yaml) (`id: trail-code`) e [bibliotecas-e-recursos.md](bibliotecas-e-recursos.md).
