# Padrões de código, Clean Code e code review

> VTX-017 · Fase F2 · Base de Conhecimento. O padrão que os **Devs** seguem ao escrever e que o **QA** usa no code review independente ([qa.md](../../agents/qa.md)). Forma do sistema e do domínio: [Arquitetura](arquitetura-de-software.md) e [DDD](padroes-de-projeto-ddd.md). Etapas 4–5 do [SOP](../processos/fluxo-entre-agentes.md).

## 1. Princípios (o que é "código limpo" na VTX)
- **Nomes que explicam:** função = verbo (`calcularHonorario`), booleano = pergunta (`estaAtivo`), termos do glossário do domínio. Se não acha nome honesto, o desenho está confuso.
- **Funções pequenas e com um motivo para mudar;** no máximo ~3 parâmetros (mais que isso → objeto/tipo).
- **Sem duplicação de regra de negócio** (DRY), mas **sem abstração especulativa** (YAGNI): extrair só na 2ª ou 3ª repetição real.
- **Erros explícitos:** validar na borda (entrada de API, formulário), falhar cedo, nunca engolir exceção; mensagem para o usuário ≠ log técnico.
- **Comentário explica o porquê,** não o quê. Regra de negócio citada com fonte (ex.: link para a norma na [pesquisa de domínio](../processos/pesquisa-de-dominio.md)).
- **Sem segredo no código:** variáveis de ambiente + `.env.example`.

## 2. Ferramentas automáticas (estilo é do robô, não do revisor)
| Linguagem | Formatador | Linter | Tipos |
|---|---|---|---|
| TypeScript/JS | [Prettier](https://prettier.io/) | [ESLint](https://eslint.org/) (config recomendada) | [`strict: true`](https://www.typescriptlang.org/tsconfig/#strict) |
| Python | [Ruff format](https://docs.astral.sh/ruff/) | Ruff (inclui [PEP 8](https://peps.python.org/pep-0008/)) | type hints + mypy em módulos de regra |
| Todos | [EditorConfig](https://editorconfig.org/) | — | — |

Tudo grátis e local, roda no pre-commit e na CI; **CI vermelha = PR não é revisado**. Commits em [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/) (`feat:`, `fix:`, `docs:`).

## 3. Tamanho e descrição do PR
- **Um PR = uma issue,** idealmente < 400 linhas alteradas (acima disso a revisão perde defeitos — [SmartBear/Cisco](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)). Maior → quebrar.
- Descrição: o quê e por quê, link da issue/história, como testar, prints se for tela, riscos.

## 4. Roteiro de code review (QA)
Dois eixos separados, para um não esconder o outro (skill [code-review](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review/SKILL.md), pin `49dd158`, em avaliação, com subagentes só locais):
1. **Especificação:** faz o que a história e os critérios de aceite pedem? Falta algo? Fez algo não pedido?
2. **Padrões:** segue este documento e as regras do repo? Depois, os **cheiros de Fowler** como juízo, nunca como regra dura: nome misterioso, código duplicado, inveja de funcionalidade, agrupamento de dados, obsessão por primitivos, switch repetido, cirurgia espalhada, generalidade especulativa ([catálogo pt-BR](https://refactoring.guru/pt-br/refactoring/smells)).
3. **Sempre olhar:** testes cobrem o critério de aceite e o caso de erro; segurança (entrada validada, autorização, dado pessoal — [OWASP](https://cheatsheetseries.owasp.org/)); desempenho óbvio (consulta em laço); nomes do domínio.

**Comentários** no formato [Conventional Comments](https://conventionalcomments.org/): `bloqueante:`, `sugestão:`, `dúvida:`, `elogio:`. Só `bloqueante` impede o merge. Comentar o código, nunca o autor.

**Bloquear quando:** critério de aceite não atendido, teste ausente para regra nova, falha de segurança, quebra de padrão documentado. Preferência pessoal não bloqueia ([Google: o padrão é melhorar a saúde do código, não a perfeição](https://google.github.io/eng-practices/review/reviewer/standard.html)). Revisor ≠ autor (nenhum agente aprova o próprio PR — [governança](../processos/governanca-e-aprovacoes.md)).

## 5. Exemplo
```ts
// Antes: nome vago, número mágico, erro engolido
function calc(v: number) { try { return v * 0.06 } catch { return 0 } }
// Depois: nome do domínio, regra com fonte, sem try inútil
const ALIQUOTA_SIMPLES_ANEXO_III = 0.06; // faixa 1, LC 123/2006 Anexo III
export function calcularImpostoSimples(receitaMensal: number): number {
  if (receitaMensal < 0) throw new RangeError("receita negativa");
  return receitaMensal * ALIQUOTA_SIMPLES_ANEXO_III;
}
```
Comentário de review: `sugestão: ALIQUOTA... depende da faixa; quando houver a 2ª faixa, virar tabela (não antes).`

## 6. Checklist do PR
- [ ] CI verde (formatador, linter, tipos, testes).
- [ ] < 400 linhas ou justificativa; descrição com issue, como testar e riscos.
- [ ] Nomes do glossário do domínio; sem número mágico; sem segredo.
- [ ] Teste para cada critério de aceite e para o caso de erro.
- [ ] Review nos 2 eixos feito por agente diferente do autor; só `bloqueante` resolvido impede merge.

## 7. Fontes
- Google, [Engineering Practices — Code Review](https://google.github.io/eng-practices/review/) e [What to look for](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- Fowler, [Code Smell](https://martinfowler.com/bliki/CodeSmell.html) · [Refactoring.Guru — cheiros de código](https://refactoring.guru/pt-br/refactoring/smells) · R. C. Martin, *Clean Code* (2008)
- [Conventional Comments](https://conventionalcomments.org/) · [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/) · [SmartBear — boas práticas de revisão](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)
