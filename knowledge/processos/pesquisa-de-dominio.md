# Pesquisa de domínio e base de conhecimento do projeto do cliente

> VTX-130 · Fase F1 · Base de Conhecimento. Etapa padrão de todo projeto de cliente, **depois da [entrevista](fluxos/entrevista-cliente.md) e antes do PRD** ([etapa 0.5 do SOP](fluxo-entre-agentes.md)). Os agentes aprendem o assunto do cliente o bastante para escrever requisitos certos e montam a base em `projects/<p>/conhecimento/`. Exemplo real: [pesquisa do med-hub](../../projects/med-hub/conhecimento/pesquisa-dominio.md).

## 1. Conceitos essenciais
- **Domínio** = a área de negócio do cliente (ex.: contabilidade médica, projetos de engenharia). Não é tecnologia.
- **Linguagem ubíqua:** os termos do cliente viram o glossário do projeto e os nomes no código ([DDD](../engenharia/padroes-de-projeto-ddd.md)).
- **Base por domínio, não por cliente:** o que vale para o setor inteiro (normas, glossário, processos) fica em `knowledge/dominios/<setor>/` e é **reaproveitado**; o que é do cliente fica em `projects/<p>/conhecimento/`.
- **Pesquisa útil** = só o que muda o produto: uma regra que obriga um campo, um fluxo que vira tela, um risco que vira requisito. O resto é curiosidade e custa tokens.

## 2. Quem, quando, entradas e saídas
| Item | Definição |
|---|---|
| Dono | **Produto** (conceitos, processos, SaaS de referência) + **Arquiteto** (integrações, riscos técnicos); **Segurança** revisa se houver dado pessoal sensível |
| Entrada | Ficha da triagem, síntese da entrevista, lista de SaaS de referência que o cliente citou |
| Saída | `projects/<p>/conhecimento/pesquisa-dominio.md` (+ `saas-<nome>.md` por referência analisada) e atualização de `knowledge/dominios/<setor>/` |
| Prazo | P/M: até 1 dia de agente; G: até 2. Passou disso, parar e registrar lacunas |
| Portão | Checklist (§6) completo → segue para o PRD |

## 3. Passo a passo
1. **Reaproveitar primeiro.** `ls knowledge/dominios/` e `grep -ril "<termo do setor>" knowledge projects`. Se o setor já tem base, ler, conferir a data e só completar o que falta (fonte com mais de 12 meses: reconferir).
2. **Perguntas de pesquisa.** Da síntese da entrevista, listar de 5 a 10 perguntas que o PRD precisa responder (ex.: "que documento a lei exige guardar e por quanto tempo?").
3. **Fontes primárias.** Lei no Planalto, resolução do conselho/agência no site oficial, documentação oficial da API. Blog só para achar a fonte primária. **Normas pagas (ABNT, ISO): só resumo com número e ano, nunca cópia** ([Lei 9.610/98](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm)).
4. **SaaS de referência.** Com o [RES](https://github.com/alextnetto/res) (pin `1d05d9c`, em avaliação) e o [Playwright MCP](https://github.com/microsoft/playwright-mcp) mapear telas, fluxos, funcionalidades e modelo de dados aparente → `saas-<nome>.md`. **Limite ([governança §5](governanca-e-aprovacoes.md)):** só comportamento público, com conta legítima; nada de contornar login, captcha ou proteção, decompilar, ou copiar texto, marca ou design. Precisa de algo além disso → Samuel.
5. **Integrações e riscos.** Arquiteto lista APIs típicas do setor (oficial? gratuita? sandbox?) e riscos técnicos (dado sensível, volume, disponibilidade de terceiros).
6. **Síntese.** Preencher o modelo (§4); cada afirmação com fonte e data de consulta. Separar **fato** (com fonte) de **hipótese** (a validar com o cliente).
7. **Promover ao domínio.** O que é genérico do setor sobe para `knowledge/dominios/<setor>/` (glossário, normas, processos) no mesmo PR.

## 4. Modelo (`projects/<p>/conhecimento/pesquisa-dominio.md`)
```markdown
# Pesquisa de domínio: <projeto> (<setor>)
Versão, data. Reaproveita: <links para knowledge/dominios/...>. Consultado em <data>.
## 1. Glossário do setor        (termo | significado | como chamar no sistema)
## 2. Normas resumidas          (norma | o que exige do produto | fonte)
## 3. Processos do setor        (fluxo atual do cliente, passo a passo)
## 4. SaaS de referência        (nome | o que copiar como ideia | o que evitar | link saas-<nome>.md)
## 5. Integrações típicas       (serviço | API oficial? | custo | uso no projeto)
## 6. Riscos do domínio         (risco | impacto | mitigação → vira requisito)
## 7. Hipóteses a validar com o cliente
## 8. Fontes                    (URL + data de consulta)
```

## 5. Exemplo resumido
Plataforma de projetos de engenharia: glossário (ART, RRT, responsável técnico); normas (Lei 6.496/77 e resoluções do CONFEA sobre ART, só resumidas); processo (projeto → revisão por profissional habilitado → ART → entrega); risco "IA assinando projeto" → requisito "só profissional com registro ativo assina". Esse glossário sobe para `knowledge/dominios/engenharia-civil/` e vale para o próximo cliente do setor.

## 6. Checklist
- [ ] Base existente do domínio procurada e reaproveitada (ou registrado que não havia).
- [ ] 5–10 perguntas de pesquisa respondidas ou marcadas como lacuna.
- [ ] Glossário com os termos usados pelo cliente na entrevista.
- [ ] Normas aplicáveis resumidas (incluindo LGPD se houver dado pessoal), sem cópia de norma paga.
- [ ] SaaS de referência analisados só pelo comportamento público, sem cópia de texto, marca ou design.
- [ ] Integrações e riscos técnicos revisados pelo Arquiteto; riscos convertidos em requisitos.
- [ ] Toda afirmação com fonte e data; hipóteses separadas para validar com o cliente.
- [ ] Parte genérica promovida para `knowledge/dominios/<setor>/`.

## 7. Fontes
- [LGPD — Lei 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) · [Lei de Direitos Autorais — 9.610/1998](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm)
- Fowler, [Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html) · Nielsen Norman Group, [Competitive Usability Evaluations](https://www.nngroup.com/articles/competitive-usability-evaluations/)
- [RES](https://github.com/alextnetto/res) (MIT) · [Playwright MCP](https://github.com/microsoft/playwright-mcp) · mattpocock, skill [research](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/research/SKILL.md) (fontes primárias, cada afirmação citada)
