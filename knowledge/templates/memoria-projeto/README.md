# Memory bank do projeto (arquivos)

> VTX-132 · Fase F12 · Ferramentas. Memória que sobrevive entre sessões, em Markdown versionado no git, lida **só quando a tarefa pedir**. Complementa o [mapa de codebase](../../engenharia/mapa-de-codebase.md) (estrutura) e os ADRs (decisões caras de reverter). Sem hooks, sem worker e sem serviço hospedado.

## 1. Conceitos essenciais
- **Memory bank** = a pasta `docs/memoria/` no repositório do projeto, copiada a partir desta pasta-modelo.
- Guarda o que a sessão seguinte precisa e que não cabe no mapa nem num ADR: jeito local, tentativa que falhou, alerta de segurança, estado do incremento aberto.
- **Ponteiro sempre carregado; arquivo sob demanda** (camada 4 de [operação de agentes](../../processos/operacao-de-agentes.md)). Colar estes arquivos numa regra always-on gasta contexto à toa.
- Segredos, tokens e dados pessoais **nunca** entram. Memória velha é pior do que memória nenhuma: quem muda o comportamento atualiza o arquivo no mesmo commit.

## 2. Arquivos

| Arquivo | Quando ler | Quando escrever |
|---|---|---|
| [padroes.md](padroes.md) | Ao implementar no assunto citado | Quando um jeito local se repetir e ainda não estiver no mapa nem num ADR |
| [decisions.md](decisions.md) | Antes de reabrir um desvio | Decisão leve, ou um ponteiro para o ADR correspondente |
| [troubleshooting.md](troubleshooting.md) | Ao bater no mesmo sintoma | Depois de um conserto não óbvio, no formato abaixo |
| [contexto-ativo.md](contexto-ativo.md) | No início de um incremento já em andamento | O que está aberto; enxugar ao fechar o incremento |
| [observacoes.md](observacoes.md) | Busca pontual por tipo ou data | Nota tipada e datada (§3) |

No projeto, o caminho canônico é `docs/memoria/`. Apague os exemplos ao copiar. Decisão que passa nos [três critérios de ADR](../../engenharia/arquitetura-de-software.md) continua em `docs/adr/`; aqui só se aponta para ela.

Formato de troubleshooting, já usado na [regra de eficiência](../cursor/eficiencia-de-tokens.mdc):

```text
[Problema] -> [Falhou] -> [Solução]
```

## 3. Observações tipadas
Cada entrada em `observacoes.md` tem data (`AAAA-MM-DD`), um tipo, um resumo de 1 a 3 linhas e, se houver, um caminho ou issue. Tipos do padrão:

| Tipo | Uso |
|---|---|
| `decision` | Escolha que a sessão seguinte precisa ver, com o motivo em uma linha |
| `bugfix` | Conserto cujo contexto se perde se ficar só no commit |
| `security_alert` | Risco ou correção de segurança; descreve o recorte e o arquivo, nunca a exploração, e nunca inclui segredo |

Outros tipos só entram se este documento for atualizado. Preferência e guardrail no estilo Trail-code ficam para a VTX-135.

## 4. Ponteiro para `AGENTS.md` ou `.cursor/rules`

Cole um bloco curto (não os arquivos). Exemplo:

```markdown
## Memória e mapa do projeto
Leitura sob demanda, nunca always-on:
- `docs/CODEBASE_MAP.md` — onboarding, ou tarefa que cruza módulos.
- `docs/memoria/contexto-ativo.md` — início de um incremento já aberto.
- `docs/memoria/padroes.md` e `docs/memoria/decisions.md` — antes de implementar ou divergir de um jeito local.
- `docs/memoria/troubleshooting.md` — ao repetir um erro (`[Problema] -> [Falhou] -> [Solução]`).
- `docs/memoria/observacoes.md` — busca por tipo (`decision`, `bugfix`, `security_alert`) ou data.
Quem mudar o comportamento atualiza o arquivo no mesmo commit. Sem hooks e sem serviço externo.
```

## 5. O que não entra neste padrão
- Hooks, notifiers, workers ou comando automático de “atualizar o bank”.
- Serviço hospedado de memória (claude-mem / CMEM Pro está **descartado**).
- Texto de `CLAUDE.md` de terceiros e qualquer trecho que cite provedor pago.

## Fontes
- Ideia dos quatro arquivos (padrões, decisões, troubleshooting, contexto ativo): [centminmod/my-claude-code-setup](https://github.com/centminmod/my-claude-code-setup/tree/7d5c374), MIT, pin `7d5c374`. Nenhum trecho copiado; os modelos foram escritos em pt-BR para o Cursor.
- Ideia de observações tipadas e datadas: [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/tree/bbb3379), Apache-2.0, pin `bbb3379`. Serviço, hooks e worker não entram.
- Memória como artefato versionado: [Operação de agentes](../../processos/operacao-de-agentes.md).
