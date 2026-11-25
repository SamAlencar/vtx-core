# Política técnica de hospedagem por cliente

> VTX-195 · 24/11/2026 · Só o lado técnico. Repasse de custo no contrato é dependência externa (agentes de vendas e de contabilidade), não aceite desta política.

## Princípios

1. **A conta de produção é do cliente**, no nome dele, com o domínio dele. A VTX não mistura produção de cliente na conta da VTX.
2. **A2 (Samuel):** o primeiro deploy de produção de um projeto, e qualquer plano pago ou upgrade (Vercel Pro, Cloudflare Pro, EAS pago, banco pago, add-on). Deploys seguintes no mesmo projeto, no plano já aprovado, seguem o runbook e não pedem A2 só por serem produção.
3. **Não violar termo de plano gratuito.** O Vercel Hobby não admite uso comercial (incluindo trabalho de consultor pago). Cliente e sites comerciais da VTX não entram no Hobby.
4. Quando o trilho de receita e o piloto interno competirem pelas [5 h/semana do Samuel](../../backlog/SCHEMA.md) (regra da F14 no SCHEMA), o de receita vem primeiro. O piloto med-hub tem teto próprio.

O passo a passo de preview do template web fica no runbook de `templates/web-next/` (VTX-194, PR #25; o arquivo entra no `main` quando esse PR for mesclado). Até lá, esta política vale sozinha. Detalhes de produto: [Vercel](../ferramentas/hospedagem/vercel.md) e [Cloudflare](../ferramentas/ci-cd/cloudflare.md).

## Quem é dono de quê

| Recurso | Padrão | Exceção |
|---|---|---|
| Conta de hospedagem de produção | Cliente (nome e faturamento dele) | Piloto interno med-hub: conta do produto/colega, não no vtx-core |
| Domínio | Cliente | Domínio da VTX só para o site da VTX |
| Preview / homologação | Mesma conta ou subconta do cliente | PoC interno não comercial pode ficar na conta da VTX (Hobby) |
| Segredos e variáveis | No painel da conta do projeto, nunca no git nem no vtx-core | — |
| DNS | Cloudflare no domínio do cliente (Free, ver ferramenta) | — |

## Tabela por tipo de produto

Limites conferidos nas fichas da base (Vercel em 27/10/2026, Cloudflare em 31/10/2026). Estouro no Hobby da Vercel **pausa o recurso por até 30 dias**. Estouro no Workers Free da Cloudflare devolve erro 1027 (a cota zera à meia-noite UTC); não é a mesma pausa, mas o site fica indisponível até o reset.

| Tipo | Hospedagem padrão | Plano gratuito com uso comercial? | Limite ou pausa a observar | Notas |
|---|---|---|---|---|
| Site / landing estática | Cloudflare Workers com *static assets* (Free); Pages continua aceitável em site já existente | Sim, com os limites do Free | Workers: 100 mil req/dia, erro 1027 no estouro; Pages: 500 builds/mês, 1 de cada vez, 20 min/build | A ficha da Cloudflare (31/10/2026) recomenda Workers com static assets para projeto novo; Pages não é proibido |
| Sistema web / Next.js de cliente | Cloudflare Workers + adaptador OpenNext (Free), **depois de testar o adaptador no primeiro projeto** | Sim, com os limites do Free | Workers Free: 100 mil req/dia, 10 ms de CPU por requisição (apertado para SSR) | O adaptador precisa ser validado (A1, ADR) no primeiro uso. Plano B se falhar ou se 10 ms não bastarem: export estático no Workers/Pages, se o app permitir; senão Vercel Pro (A2). Vercel Hobby **não** entra |
| API | Cloudflare Workers (Free) | Sim, com os limites do Free | 100 mil req/dia; ao estourar, 1027 até o reset | Plano pago é A2 |
| App Expo | EAS Preview no plano gratuito | A verificação do termo atual do EAS é da VTX-203 (template Expo), não desta política | Build de preview no plano free | Produção paga no EAS é A2 |
| Agente de IA / IA embutida | Igual ao sistema web, mais teto de custo do provedor de modelo | Infra de app: sim no Cloudflare Free | Além da cota de hospedagem, o custo de token é outro (A2 se for plano pago) | O teto contratual é dependência externa |
| Piloto interno med-hub | Igual ao sistema web / Next.js de cliente | Sim | Iguais ao sistema web | Não usar Vercel Hobby: o med-hub é produto em uso, não PoC interno da VTX. Não há cobrança da VTX neste piloto |
| Ferramenta interna da VTX, sem receita | Vercel Hobby | Não se aplica (uso não comercial) | 100 GB transferência, 1 mi req CDN, 4 h CPU/mês; estouro pausa até 30 dias | Único caso em que o Hobby é o padrão |

## Custos de infra (só registrar)

No runbook do repositório do cliente, anotar: provedor, plano, dono da conta, domínio, e o que já se sabe de cota. Qualquer upgrade é A2. Quem cobra o cliente pelo repasse é trabalho dos agentes de vendas e de contabilidade, não deste repositório.

## Checklist (DevOps)

- [ ] Conta e domínio no nome do cliente (ou do piloto, no caso do med-hub)
- [ ] Plano gratuito permitido para uso comercial, ou A2 para plano pago
- [ ] Variáveis só no painel; nada de segredo no git
- [ ] Limite de cota e o que acontece no estouro (pausa ou 1027) escritos no runbook
- [ ] Primeiro deploy de produção é A2; plano pago ou upgrade também é A2
