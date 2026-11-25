# Catálogo de ferramentas da VTX

> VTX-098 · Fase F12 · Base de Conhecimento. Este documento mostra **como usar** cada ferramenta e **como ela entra nos fluxos**. A **escolha** da stack padrão fica no [stack de referência](../tecnologia/stack-de-referencia.md) (VTX-023), e a do ambiente dos agentes na VTX-062. Aqui não se repete o que já estiver lá: o catálogo só aponta para esses documentos.

## 1. Estrutura
- Um arquivo por ferramenta: `knowledge/ferramentas/<categoria>/<ferramenta>.md` (ex.: `hospedagem/vercel.md`).
- Quando duas ferramentas concorrem pelo mesmo uso, elas ficam em um arquivo comparativo (ex.: `pagamentos/stripe-mercado-pago.md`).
- Cada ferramenta adotada tem um **registro de adoção** (§4) no próprio arquivo.
- Bibliotecas, skills, regras e servidores MCP usados pelos agentes: [bibliotecas-e-recursos.md](bibliotecas-e-recursos.md) e [recursos.yaml](recursos.yaml).
- Status: `adotada` (padrão VTX), `em avaliação`, `alternativa` (só com motivo), `descontinuada`.

## 2. Categorias
| Categoria | Pasta | Exemplos |
|---|---|---|
| Hospedagem e deploy | `hospedagem/` | Vercel, Cloudflare Pages, GitHub Pages, Netlify |
| Backend, BaaS e banco | `backend/` | Supabase, Appwrite, Firebase, PostgreSQL |
| Autenticação | `auth/` | Supabase Auth, Appwrite Auth, Firebase Auth, Clerk |
| Pagamentos | `pagamentos/` | Stripe, Mercado Pago |
| Observabilidade | `observabilidade/` | Sentry, logs da hospedagem, uptime |
| CI/CD e infraestrutura | `ci-cd/` | GitHub, GitHub Actions, Docker, Cloudflare (DNS, WAF, Access) |
| Mobile | `mobile/` | Expo / EAS |
| Design | `design/` | Figma |
| IA e desenvolvimento | `ia-dev/` | Cursor (regras, agentes locais e na nuvem), Grok Bot |
| Comunicação e gestão | `comunicacao/` | Google Workspace (Drive, Gmail, Agenda), chat do Grok Bot |

## 3. Modelo de documento por ferramenta
```markdown
# <Ferramenta>
> Categoria · Status (adotada | em avaliação | alternativa | descontinuada) · Revisado em AAAA-MM-DD
## 1. O que é            — 2 a 3 linhas
## 2. Quando usar / quando não usar
## 3. Alternativas       — tabela curta e motivo da escolha
## 4. Custo e plano gratuito — limites que importam, quando começa a cobrança (alerta: custo novo = Samuel)
## 5. Nos fluxos         — tabela: fluxo × etapa × uso (SaaS, mobile, API, site, manutenção, MVP/PoC)
## 6. Papel responsável  — quem configura, quem usa, quem revisa (ver agents/)
## 7. Setup              — passos mínimos, CLI, integração com GitHub/CI
## 8. Segredos e segurança/LGPD — onde ficam as chaves (secrets, nunca no repo/chat), região dos dados, DPA, permissões mínimas
## 9. Checklist          — pronto para usar em projeto
## 10. Registro de adoção (§4) e Fontes — documentação oficial com data
```

## 4. Critérios para adotar uma ferramenta nova (registro de decisão)
Para adotar uma ferramenta, registra-se no arquivo dela (formato ADR curto: contexto, opções, decisão, consequências):
1. **Necessidade real** em um fluxo. Nada de ferramenta "para o futuro".
2. **Plano gratuito ou custo baixo e previsível.** Qualquer custo recorrente ou cartão de crédito vai para o **Samuel**.
3. **Segurança e LGPD:** região dos dados, DPA ou termos de tratamento, 2FA e tokens de escopo mínimo.
4. **Saída fácil:** exportação de dados e padrões abertos (SQL, Docker, Git), para evitar ficar preso ao fornecedor.
5. **Uso por agentes:** tem CLI, API ou MCP, e boa documentação.
6. **Sobreposição:** o que a ferramenta substitui do catálogo atual. Uma ferramenta por uso, salvo motivo escrito.

O Orquestrador e o Arquiteto decidem as ferramentas `em avaliação` e `alternativa`. Passar uma ferramenta para `adotada` com custo, dados pessoais ou contrato exige aprovação do Samuel.

## 5. Matriz ferramenta × fluxo
<a id="matriz"></a>

Legenda: **P** = padrão do fluxo · **O** = opcional ou alternativa · **—** = não se aplica.

Preenchida em 2026-11-24 (VTX-112) só com o que já está documentado: a §5 de cada ferramenta e o esqueleto do VTX-098. Sem ferramenta nova. [Avaliações](avaliacoes/graphify.md) e o [radar](radar.md) ficam de fora até haver registro de adoção. A **escolha** formal da stack continua no [stack de referência](../tecnologia/stack-de-referencia.md) e no ADR do projeto.

| Ferramenta | [SaaS](../processos/fluxos/sistema-web-saas.md) | [Mobile](../processos/fluxos/app-mobile.md) | [API](../processos/fluxos/api-integracoes.md) | [Site](../processos/fluxos/site-landing-page.md) | [Manutenção](../processos/fluxos/manutencao-evolucao.md) | [MVP/PoC](../processos/fluxos/mvp-poc.md) |
|---|---|---|---|---|---|---|
| [GitHub + Actions](ci-cd/github-actions.md) | P | P | P | P | P | P |
| [Cursor](ia-dev/cursor.md) | P | P | P | P | P | P |
| [Vercel](hospedagem/vercel.md) | O | — | O | O | O | O |
| [Cloudflare](ci-cd/cloudflare.md) | P | — | P | P | O | O |
| [Supabase](backend/supabase.md) | P | P | P | O | O | O |
| [Appwrite](backend/appwrite.md) | O | O | O | — | O | O |
| [Firebase](backend/firebase.md) | O | O | — | — | O | O |
| [Expo / EAS](mobile/expo.md) | — | O | — | — | O | O |
| [Stripe / Mercado Pago](pagamentos/stripe-mercado-pago.md) | P | P | P | — | O | P |
| [Sentry](observabilidade/sentry.md) | P | P | P | — | P | O |
| [Docker](ci-cd/docker.md) | P | — | P | — | O | O |
| [Figma](design/figma.md) | P | P | — | P | O | O |
| [Google + Grok Bot](comunicacao/google-workspace.md) | O | O | O | O | O | O |

Notas (células que não são um P óbvio):
- **Vercel** está em avaliação. Hobby não cobre uso comercial; site estático vai para GitHub Pages ou Cloudflare Pages; Pro/comercial é decisão do Samuel.
- **Appwrite** e **Firebase** não são o backend padrão (é o Supabase). Entram se o cliente já usa ou pedir. No mobile, o Firebase pode entrar só para FCM e Crashlytics, mesmo com backend Supabase.
- **Expo / EAS** só quando o ADR de mobile escolhe React Native.
- **Supabase** no site só para guardar leads (com consentimento). Na manutenção e no MVP, só se o sistema tiver backend.
- **Stripe** na manutenção só se o sistema já cobra. **Sentry** no MVP é opcional (não aparece na §5 da ferramenta).
- **Cloudflare** na manutenção: DNS e proteção de domínio já existente (o status da ferramenta cobre todo domínio; a §5 não cita esse fluxo).
- **Google + Grok Bot** é o canal da operação. Na [entrevista com o cliente](../processos/fluxos/entrevista-cliente.md) entram Agenda, Meet e ata no Drive.

## 6. Revisão periódica
Uma vez por trimestre, dentro da manutenção quinzenal (VTX-113), revisam-se custos, limites dos planos gratuitos, versões e mudanças de preço, incidentes de segurança e ferramentas sem uso. Status e datas são atualizados, e o que muda custo ou contrato vai para o Samuel.

## Checklist
- [x] Estrutura, categorias, modelo, critérios e esqueleto da matriz
- [x] Um documento por ferramenta (VTX-099 a VTX-111): [Vercel](hospedagem/vercel.md), [Supabase](backend/supabase.md), [GitHub Actions](ci-cd/github-actions.md), [Cursor](ia-dev/cursor.md), [Appwrite](backend/appwrite.md), [Firebase](backend/firebase.md), [Expo](mobile/expo.md), [Stripe/MP](pagamentos/stripe-mercado-pago.md), [Sentry](observabilidade/sentry.md), [Cloudflare](ci-cd/cloudflare.md), [Docker](ci-cd/docker.md), [Figma](design/figma.md), [Google + Grok Bot](comunicacao/google-workspace.md)
- [x] Matriz completa (VTX-112)
- [ ] Processo de revisão (VTX-113)

## Fontes
- Nygard, M. *Documenting Architecture Decisions* (2011): formato ADR.
- ThoughtWorks Technology Radar: categorias adotar / avaliar / evitar.
- Documentação oficial de cada ferramenta, citada no documento dela.


## Radar
Até o piloto começar, ferramentas novas vão para o [radar](radar.md), não para o backlog (decisão de 23/10/2026).
