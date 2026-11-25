# Mapa de codebase por projeto

> VTX-131 · Fase F12 · Ferramentas. Padrão do `docs/CODEBASE_MAP.md` de cada repositório: um índice curto, escrito por agente local, para a sessão seguinte não reler o repo inteiro. Complementa o [documento de arquitetura](arquitetura-de-software.md) (decisões e C4) e o [memory bank](../templates/memoria-projeto/README.md) (padrões, decisões leves e lições). A ideia de um mapa por projeto veio de uma ferramenta **sem licença** (ver Fontes); este texto e o modelo foram escritos do zero, sem reaproveitar frase ou código.

## 1. Conceitos essenciais
- **Mapa** = índice navegável: o que o sistema é, por onde se entra, quais módulos existem, como os fluxos principais caminham. Não substitui o `docs/arquitetura.md` nem os ADRs.
- **Fonte de verdade:** o código. Se o mapa divergir, vale o código, e o mapa se atualiza no mesmo incremento.
- **Carga sob demanda:** `AGENTS.md` ou uma regra do Cursor só apontam o caminho e *quando* ler (onboarding, ou tarefa que cruza módulos). O mapa não entra em regra always-on.
- **Agente local:** quem gera e atualiza é o Arquiteto ou o Dev do stack, no próprio repositório. Sem agente de nuvem e sem copiar ferramenta sem licença.

## 2. Metodologia

### 2.1 Quando criar
- Repositório novo: no incremento em que a estrutura já existe, junto ou logo depois de `docs/arquitetura.md`.
- Repositório já existente: na primeira sessão de onboarding ou de manutenção que precise de uma visão do todo.

### 2.2 Como gerar
1. Ler o README, os manifests (`package.json`, `pyproject.toml`, `go.mod` etc.), o `docs/arquitetura.md` e os ADRs, se existirem.
2. Listar pastas de primeiro nível respeitando `.cursorignore` e artefatos gerados (`node_modules/`, `dist/`, `.next/`, `coverage/`, `build/`).
3. Em cada módulo, abrir só o ponto de entrada e a interface pública. Não varrer todos os arquivos.
4. Preencher o modelo da §3. O que não estiver claro fica como “a confirmar”. Não inventar módulo, fluxo ou dependência.
5. Incluir o mapa no mesmo PR da estrutura, ou num PR só de documentação se for onboarding.

### 2.3 Quando atualizar
No fim do incremento, atualizar **só as seções afetadas** (não reescrever o arquivo) se mudou módulo, ponto de entrada, fluxo principal, dependência entre partes ou pasta movida. Correção interna, typo ou teste pontual que não altera a interface pública não exigem atualização. O cabeçalho leva a data e o SHA do commit em que o mapa foi conferido.

### 2.4 O que não fazer
- Não copiar texto ou código de ferramenta sem licença — em especial [kingbootoshi/cartographer](https://github.com/kingbootoshi/cartographer) (pin `a62d169`).
- Não exigir subagentes pagos nem varrer o repositório inteiro “para ficar completo”.
- Não versionar grafo gerado por ferramenta até o piloto da VTX-135 (Trail-code). O Markdown basta.

## 3. Modelo (`docs/CODEBASE_MAP.md`)

```markdown
# Mapa de codebase — <nome do projeto>

Atualizado em: AAAA-MM-DD · Conferido no commit: <sha curto>
Leitura: sob demanda. Se este arquivo divergir do código, vale o código; atualize o mapa no mesmo incremento.

## Visão
<um parágrafo: o que o sistema faz, estilo (ex.: monólito modular) e onde roda>
Arquitetura: ver `docs/arquitetura.md` (C4 e ADRs).

## Pontos de entrada
| Entrada | Caminho | Como sobe / dispara |
|---|---|---|
| <app web, API, worker, CLI> | `<caminho>` | <comando, rota ou cron> |

## Módulos
### `<nome>` (`<caminho>/`)
- Responsabilidade: <uma frase>
- Interface pública: <arquivos ou símbolos que o resto do repo deve usar>
- Depende de: <módulos ou serviços>
- Usado por: <quem chama>
- Arquivos-chave: <3 a 7 caminhos; não a lista completa>

## Fluxos principais
- <2 a 5 fluxos em uma linha, ou um Mermaid curto: “pedido web → API → banco”>

## Convenções e armadilhas
- <só o que não é óbvio: exceção à regra, ordem de boot, pasta gerada>

## Fora do mapa
- <vendor, fixtures pesados, gerado; o que o agente não lê por padrão>
```

## 4. Exemplo
“Agenda para clínicas” (o mesmo do [documento de arquitetura](arquitetura-de-software.md)). Visão: monólito modular em Next.js + API Node + PostgreSQL, um tenant por clínica. Pontos de entrada: `apps/web` (Next.js), `apps/api` (HTTP) e `apps/worker` (lembretes). Módulos: `agenda` (regras de conflito; interface `servicos/agenda.ts`), `pacientes` e `lembretes`. Fluxo principal: recepção marca horário na web → API valida conflito → grava no banco → worker dispara e-mail. Fora do mapa: `.next/`, dumps de demonstração. O C4 e os ADRs ficam em `docs/arquitetura.md`; lições de sessão, no [memory bank](../templates/memoria-projeto/README.md).

## 5. Checklist
- [ ] `docs/CODEBASE_MAP.md` existe; `AGENTS.md` ou regra do Cursor aponta o caminho e diz quando ler
- [ ] Cabeçalho com data e SHA
- [ ] Pontos de entrada, módulos e fluxos preenchidos; nada inventado
- [ ] Incremento que muda estrutura atualiza só as seções afetadas, no mesmo PR
- [ ] Sem texto ou código de ferramenta sem licença; sem agente de nuvem

## Fontes
- Ideia apenas (não o texto nem o código): [kingbootoshi/cartographer](https://github.com/kingbootoshi/cartographer/tree/a62d169), pin `a62d169`. Sem licença declarada (API `/license` retornou 404 em 24/11/2026). Não copiar.
- C4 e `docs/arquitetura.md`: [Arquitetura de software](arquitetura-de-software.md).
- Ponteiros e divulgação progressiva: [Operação de agentes](../processos/operacao-de-agentes.md) · [agents.md](https://agents.md).
- Piloto futuro de grafo local: VTX-135 (Trail-code), ainda não adotado.
