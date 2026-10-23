# Estratégia de testes e qualidade

> VTX-018 · Fase F2 · Base de Conhecimento. O que o **QA** ([qa.md](../../agents/qa.md)) planeja e cobra, e o que os **Devs** entregam junto com o código. Liga [requisitos](../processos/engenharia-de-requisitos.md) (critérios de aceite) ao [code review](padroes-de-codigo.md) e à [CI](git-e-ci-cd.md).

## 1. Conceitos
- **Pirâmide de testes:** muitos testes de **unidade** (rápidos, isolados), alguns de **integração** (banco, API real em contêiner local), poucos **E2E** (fluxo do usuário no navegador). Inverter a pirâmide deixa a suíte lenta e instável ([Fowler](https://martinfowler.com/articles/practical-test-pyramid.html)).
- **Critério de aceite → teste:** cada Given/When/Then da história vira pelo menos um teste automatizado; é a ponte entre o PRD e o código.
- **TDD (vermelho → verde → refatorar):** obrigatório em regra de negócio (cálculo, permissão, estado); opcional em tela e cola de integração.
- **Qualidade ≠ só teste:** linter, tipos, revisão e testes de segurança fazem parte (modelo de qualidade da ISO/IEC 25010, só citado: adequação funcional, confiabilidade, usabilidade, segurança, manutenibilidade, desempenho).

## 2. Ferramentas (grátis, open source, locais)
| Camada | TypeScript/React/RN | Python |
|---|---|---|
| Unidade/integração | [Vitest](https://vitest.dev/) (+ [Testing Library](https://testing-library.com/)) · Jest no React Native | [pytest](https://docs.pytest.org/) |
| E2E web | [Playwright](https://playwright.dev/) (já avaliado no catálogo) | Playwright for Python |
| Banco real em teste | [Testcontainers](https://testcontainers.com/) ou Supabase local (CLI) | idem |
| Cobertura | `vitest --coverage` (v8) | [coverage.py](https://coverage.readthedocs.io/) |
| Acessibilidade | [axe-core](https://github.com/dequelabs/axe-core) dentro do Playwright | — |

## 3. Metodologia (por história)
1. **Planejar** (QA, na refinação): listar os critérios de aceite e o caso de erro de cada um em `projects/<proj>/testes/plano.md`.
2. **Escrever o teste antes** da regra (Dev, TDD); nome do teste = comportamento (`deve recusar receita negativa`).
3. **Integração** para tudo que cruza fronteira (API ↔ banco, autenticação, RLS do Supabase): banco real local, nunca mock do banco.
4. **E2E** só para os fluxos críticos (login, cadastro principal, pagamento/fechamento): 5–15 por projeto.
5. **CI verde** é pré-requisito do review. Teste instável (*flaky*) é defeito: corrigir ou colocar em quarentena com issue em até 1 dia.
6. **Defeito achado** → primeiro um teste que reproduz, depois a correção (não volta).

## 4. Metas objetivas
- Cobertura de linhas ≥ **80 % nos módulos de regra de negócio**; sem meta global (cobertura alta com asserção fraca não vale). [Teste de mutação](https://stryker-mutator.io/) é opcional para módulos críticos.
- Suíte de unidade < 2 min; E2E < 10 min na CI.
- Severidade do defeito: **crítico** (perda de dado, segurança, bloqueio) bloqueia release; **alto** bloqueia o PR; **médio/baixo** vira issue.

## 5. Exemplo (Vitest, critério de aceite → teste)
```ts
// HU-07: Dado receita mensal de 10.000, Quando calcular, Então imposto = 600
import { describe, it, expect } from "vitest";
import { calcularImpostoSimples } from "./imposto";
describe("calcularImpostoSimples", () => {
  it("aplica 6% na faixa 1 (HU-07)", () => expect(calcularImpostoSimples(10_000)).toBe(600));
  it("recusa receita negativa", () => expect(() => calcularImpostoSimples(-1)).toThrow(RangeError));
});
```

## 6. Checklist
- [ ] `testes/plano.md` lista critérios de aceite e casos de erro.
- [ ] Cada critério tem teste; regra nova nasceu com TDD.
- [ ] Integração usa banco real local; E2E só nos fluxos críticos.
- [ ] Cobertura ≥ 80 % nos módulos de regra; nenhum teste instável sem issue.
- [ ] Defeito corrigido veio com teste de regressão.

## 7. Fontes
- Fowler/Vocke, [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) · Fowler, [Test Coverage](https://martinfowler.com/bliki/TestCoverage.html)
- Google Testing Blog, [Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)
- K. Beck, *Test-Driven Development: By Example* (2002) · ISO/IEC 25010 (norma paga: só citada, não copiada)
- Docs: [Vitest](https://vitest.dev/), [Playwright](https://playwright.dev/), [pytest](https://docs.pytest.org/), [Testing Library](https://testing-library.com/)
