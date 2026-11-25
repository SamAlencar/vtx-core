---
name: diagramas
description: "Use ao criar ou revisar um diagrama editorial (arquitetura, fluxograma de decisão, sequência) em HTML + SVG autocontido para ADRs, docs e sites da VTX. Não use para rascunho em Markdown — isso é Mermaid."
license: MIT
---

# Diagramas editoriais (VTX)

Diagramas em HTML com SVG embutido, tema VTX e fontes locais. Adaptação MIT do [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design), pin `7a12007` — ver `NOTICE.md` e `LICENSE`.

## Quando usar

Use quando o leitor aprende mais com o desenho do que com um parágrafo ou uma tabela: decisão de ADR, recorte de arquitetura, troca de mensagens entre atores.

Não use para lista, tabela, rascunho de PR ou um único conceito (escreva a frase). Não misture Mermaid e esta skill como fonte de verdade no mesmo ADR: Mermaid fica no rascunho; o diagrama editorial é o artefato.

## Regras

- O melhor passo costuma ser apagar. Um nó = uma ideia. Acima de 9 nós, quase sempre são dois diagramas.
- Um ou dois nós focais por figura, na cor de acento. O acento em cinco nós deixa de sinalizar.
- Autocontido: CSS do tema copiado no `<style>`, sem `fonts.googleapis.com`, sem script, sem rede.
- Fontes: `system-ui`, `"Segoe UI"`, `"Liberation Sans"` (e a pilha mono equivalente). Não usar Inter, Geist nem qualquer webfont remota.
- Tema: copiar os tokens de `tema-vtx.css`. Não voltar ao padrão do diagram-design (paper `#f5f5f5`, coral `#bf4520`). O tema é provisório até haver marca oficial; não invente outra paleta por diagrama.
- Texto em português, contraste AA no papel e no nó focal (tinta clara no acento).
- Comece por um dos templates em `templates/` e troque só o conteúdo.
- Não execute scripts do repositório de origem. PNG, se um dia for preciso, sai do Playwright local já adotado.

## Tipos nesta skill

| Se o desenho mostra… | Tipo | Template |
|---|---|---|
| Partes e conexões de um sistema, numa foto só | Arquitetura | `templates/arquitetura.html` |
| Decisão com ramos (aceito / recusado) | Fluxograma | `templates/fluxograma.html` |
| Mensagens no tempo, entre atores | Sequência | `templates/sequencia.html` |

Outros 40+ tipos do projeto de origem não foram copiados. Se um ADR pedir algo fora dessa lista, estenda com o mesmo tema e registre no `NOTICE.md`; não traga o script nem o Google Fonts.

## Checklist antes de entregar

- [ ] Abre no navegador sem rede e sem erro de fonte.
- [ ] Não há `fonts.googleapis.com` nem `@import` remoto.
- [ ] Tokens iguais aos de `tema-vtx.css`.
- [ ] Título, nós e legendas em português; 1–2 focais.
- [ ] Ligado a partir do ADR ou doc que ilustra.
- [ ] `LICENSE` / `NOTICE.md` intactos se a skill for copiada para outro repo.

## Exemplos no med-hub

Os quatro ADRs de `projects/med-hub/docs/adr/` têm diagramas em `projects/med-hub/docs/adr/diagramas/`.
