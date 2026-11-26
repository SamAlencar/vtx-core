# Orientações de agentes de IA do Samuel: mapeamento no vtx-core

> VTX-221 · Fase F1 · Processo. Mapeamento das orientações do Samuel sobre agentes de IA (topologia, contexto, porta para produção e segurança) contra o que o vtx-core já tem. Só a parte técnica deste repositório; vendas, contrato e operação comercial ficam com os outros agentes. Data: 26/11/2026.

## 1. Lacunas do texto de origem

O registro da mensagem do Samuel chegou truncado. Trabalhou-se só com o que havia:

- **Item 2 (arquitetura de contexto):** só a primeira frase ("instruções como código versionado no Git, separadas por escopo: AGENTS.md, SKILL.md, DESIGN.md"). O resto da seção não chegou.
- **Item 3:** não existe no registro (a numeração vai de 2 para 4).
- Quando o texto completo aparecer, revisar este mapeamento e as VTX-221 a VTX-224.

## 2. Mapeamento

Ação: **atende** (nada a fazer), **ampliar VTX-xxx** (item existente ganha escopo, sem ID novo), **nova VTX-22x** ou **adiado** (com motivo).

| # | Orientação | Estado no vtx-core | Ação |
|---|---|---|---|
| 1.1 | Decompor responsabilidades, sem agente faz-tudo | Papéis em [papeis-de-agentes.md](../organizacao/papeis-de-agentes.md) e `agents/*.md`; SOP com um dono por etapa e "quem produz não aprova" ([fluxo-entre-agentes.md](fluxo-entre-agentes.md)) | **Atende** |
| 1.2 | Orquestrador + subagentes especializados que validam entregas | Orquestrador existe; subagente só citado para pesquisa ([operacao-de-agentes.md](operacao-de-agentes.md) §5); revisor independente (Tzu) é prática, sem documento | **Nova VTX-221:** [topologia-de-agentes.md](topologia-de-agentes.md) §2 |
| 1.3 | Critério: agente novo × ferramenta/subagente | Não havia | **Nova VTX-221:** topologia §3 |
| 1.4 | Modelos por perfil (forte para aceite, arquitetura e revisão; rápido para implementação guiada por testes) | Não havia. A VTX-148 trata roteamento de modelo **dentro do produto do cliente**, não dos agentes da VTX | **Nova VTX-221:** topologia §4 |
| 2.1 | Instruções como código versionado, por escopo | `AGENTS.md` raiz, `.cursor/rules/` com `globs`, `agents/<papel>.md` e `.cursor/skills/*/SKILL.md`, todos no Git, com teste de caminhos (`tests/test_agents_md.py`) | **Atende** (tabela de escopos na topologia §5) |
| 2.2 | `DESIGN.md` | Não existe. Só faz sentido onde há interface: o template web (`templates/web-next/`, PR #25) | **Ampliar VTX-210** (regras de engenharia do template web): incluir `DESIGN.md` |
| 2.3 | `AGENTS.md` por camada de código | Só o da raiz e o dos templates | **Ampliar VTX-212** (fronteira de camadas): `AGENTS.md` curto em `src/dominio/` e `src/agentes/` |
| 4.1 | CI bloqueia o PR; o agente corrige build/lint | CI informativo (sem proteção de branch no plano gratuito); não há lint/tipos Python no CI | **Ampliar VTX-214** (portão de merge por script) e **VTX-215** (ruff/mypy no CI, com `ruff --fix` local como autofix). Regra do laço de autofix: [porta-para-producao.md](porta-para-producao.md) §2 |
| 4.2 | Revisão cruzada por IA com contexto limpo e modelo diferente | Prática do Tzu nos PRs (veredito na HEAD), sem documento | **Nova VTX-222:** porta §3. **Ampliar VTX-214:** o script confere o veredito na HEAD exata |
| 4.3 | Revisão humana calibrada por risco + smoke tests | Etiqueta "precisa do Samuel" e A2 na [governança](governanca-e-aprovacoes.md); VTX-172 (revisão obrigatória) está `aguardando` decisão do Samuel | **Nova VTX-222:** porta §4 (classes de risco). Merge automático de PR trivial **adiado** até a VTX-214 existir |
| 4.4 | Validação em staging para mudança crítica | Preview gratuito descrito na [política de hospedagem](../operacao/hospedagem-por-cliente.md); sem staging nos templates | **Adiado:** depende do template web (VTX-194) e da e2e do template (VTX-217, da auditoria); regra já escrita na porta §4 |
| 5.1 | Execução isolada (contêiner descartável, sem segredos locais) | VTX-147 (sandbox para código gerado por IA, `a fazer`) | **Ampliar VTX-147:** incluir a execução dos próprios agentes de desenvolvimento num contêiner local descartável (Docker Engine, grátis) |
| 5.2 | Deny rules explícitas (`.env`, chaves, comandos destrutivos, force push) | `.cursorignore` não bloqueia `.env` nem chaves (o texto de [cursor.md](../ferramentas/ia-dev/cursor.md) §8 diz que sim); não há `.cursor/cli.json` | **Nova VTX-224**, no PR #28 com "precisa do Samuel" (mexe em permissões de agente) |
| 5.3 | Auditar skills de terceiros como dependência | Regra geral em [bibliotecas-e-recursos.md](../ferramentas/bibliotecas-e-recursos.md) ("tratar skill de comunidade como biblioteca") | **Nova VTX-223:** checklist em [auditoria-de-skills.md](../seguranca/auditoria-de-skills.md) |

## 3. Relação com a auditoria técnica (25/11/2026)

Os itens da auditoria VTX-210, VTX-212, VTX-214 e VTX-215 entraram no backlog mestre com o texto da auditoria e as ampliações acima nas `notas`. A ordem dos P0 continua: VTX-194 (PR #25) → VTX-210 → VTX-212 → VTX-177. Nada deste mapeamento passa na frente desses itens: as VTX-221 a 223 são só documento, e a VTX-224 não depende de P0. Os demais itens da auditoria (VTX-211, 213, 216 a 220) seguem reservados e não foram importados aqui.

## 4. Checklist

- [x] Cada orientação com estado e ação
- [x] Lacunas do texto de origem registradas
- [x] Sobreposição com a auditoria tratada como ampliação, sem ID duplicado
- [ ] Revisar quando o texto completo das orientações aparecer

## Fontes

- Auditoria técnica de 25/11/2026 (`auditoria-tecnica-cursor.md`, §4, fora do repositório).
- Orientações do Samuel sobre agentes de IA (repassadas em 26/11/2026; registro truncado).
