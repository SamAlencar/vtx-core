# Sandbox Impeccable (VTX-127)

Piloto do [pbakaus/impeccable](https://github.com/pbakaus/impeccable) ([site](https://impeccable.style)) numa tela de teste, com versão fixada. Não é um produto VTX.

**Decisão: adotado com restrições.** O detector determinístico e a skill (cópia pinada, sob demanda) entram no fluxo de frontend. `npx impeccable install`, hooks automáticos, login e recursos Pro ficam de fora. Relato no `recursos.yaml` e em [bibliotecas-e-recursos.md §3.10](../../knowledge/ferramentas/bibliotecas-e-recursos.md).

## Conceitos

O impeccable tem duas camadas:

1. **Detector** — binário nativo (engine 0.1.27, ~25 MiB no linux-x64) com 62 regras determinísticas (slop, contraste, tipografia). Roda localmente, sem LLM. No pin `b49177d` o pacote npm é 4.10.0; a ponta do npm em 24/11/2026 já era 4.11.0 — o piloto ficou no pin.
2. **Skill e comandos** — `SKILL.md` (~3,2 mil tokens) e 50 arquivos de referência (~125 mil tokens se carregados todos). Os comandos (`init`, `shape`, `critique`, `audit`…) orientam o agente; as referências só devem entrar sob demanda.

O instalador (`npx impeccable install`) copia a skill e grava um hook `postToolUse` em todo `Write`, com timeout de 5 s, que executa o engine. O CLI baixa o binário de GitHub Releases (ou do pacote opcional `@impeccable/cli-<os>-<arch>`), confere SHA-256 contra `engine-checksums.txt` e recusa download sem manifesto. A telemetria vem **ligada por padrão**; desliga com `DO_NOT_TRACK=1`, `IMPECCABLE_NO_TELEMETRY=1` ou `impeccable telemetry off`. Upload de “health” só ocorre com login. Há camada de conta e regras Pro — fora da política da VTX.

O código do engine está no mesmo repositório (Apache-2.0, pasta `crates/`). Mesmo assim é um binário pré-compilado: só roda depois da conferência do checksum do pin.

## Metodologia

Revisão no clone `/tmp/impeccable-review/repo` no commit `b49177d` (licença, `cli/bin/cli.js`, `scripts/fetch-engine.mjs`, `.cursor/hooks.json`, `cursor-plugin/hooks/hooks.json`, `crates/context/src/telemetry.rs`, `crates/cli/src/router.rs`) **antes** de baixar o binário. Nada de `npx impeccable install` no vtx-core.

No sandbox: `scripts/rodar-detector.sh` baixa só `impeccable-linux-x64` 0.1.27, confere o SHA-256 `41d66e945bcdfc560005b61ad0b6b2312b124890039262f2e63322ef2709ccfd` (manifesto do pin), exporta `DO_NOT_TRACK=1` e `IMPECCABLE_NO_TELEMETRY=1`, aponta `IMPECCABLE_HOME` para `.impeccable-home/` (gitignorado) e roda `detect --json` em `tela-teste/index.html`. Sem login. Binário, cache e JSON bruto ficam fora do git. O código 2 do detector significa “achados”, não falha de execução.

Não houve A/B de tokens de um passe completo de crítica com e sem a skill: isso exigiria um segundo agente e não seria um número honesto neste ambiente. O que deu para medir está nos resultados abaixo.

## Exemplos

A página `tela-teste/index.html` é um “AI slop” proposital: Inter, degradê roxo–azul, texto cinza `#9ca3af` no fundo colorido, ícone 56×56 acima do H1 e três cards. Em 24/11/2026 o detector 0.1.27, em **0,049 s** e **0 tokens de LLM**, apontou cinco avisos (saída sanitizada em `exemplos/detect-saida.json`):

| Regra | Categoria | O que pegou |
|---|---|---|
| `gray-on-color` | quality | texto `#9ca3af` no degradê `#7c3aed`–`#2563eb` |
| `low-contrast` | quality | contraste 2,0:1 (precisa 4,5:1) |
| `icon-tile-stack` | slop | tile 56×56 acima do H1 |
| `overused-font` | slop | Inter como fonte principal |
| `ai-color-palette` | slop | acentos roxo/violeta |

O binário medido tem 26 051 472 bytes. `impeccable telemetry status` confirmou *off* por `DO_NOT_TRACK`. Não foi criado `~/.impeccable`. `detect --list-rules` listou as 62 regras do pin.

## Checklist (agente)

- [ ] Usar o detector só em tela de frontend, com o script (ou o mesmo pin, checksum e variáveis de opt-out).
- [ ] Não rodar `npx impeccable install` no vtx-core nem em projeto de cliente.
- [ ] Não gravar hooks `postToolUse` automaticamente.
- [ ] Não fazer login, não ligar `health`, não usar regras Pro.
- [ ] Copiar `SKILL.md` só com o pin `b49177d` e só quando o fluxo de frontend pedir; referências sob demanda, não a árvore inteira de ~125 mil tokens.
- [ ] Conferir SHA-256 de qualquer engine novo contra o manifesto do pin antes de executar.
- [ ] Manter `DO_NOT_TRACK=1` e `IMPECCABLE_NO_TELEMETRY=1`.

## Fontes

- Repositório, pin `b49177d`: https://github.com/pbakaus/impeccable
- Site: https://impeccable.style
- Release do engine 0.1.27: https://github.com/pbakaus/impeccable/releases/tag/engine-v0.1.27
- Pacote npm (ponta, conferir o pin): https://www.npmjs.com/package/impeccable
- Registro: [recursos.yaml](../../knowledge/ferramentas/recursos.yaml) (id `impeccable`) e [bibliotecas-e-recursos.md §3.10](../../knowledge/ferramentas/bibliotecas-e-recursos.md)
- Checklist de skill/hook/npx: [bibliotecas-e-recursos.md §3.13](../../knowledge/ferramentas/bibliotecas-e-recursos.md)
