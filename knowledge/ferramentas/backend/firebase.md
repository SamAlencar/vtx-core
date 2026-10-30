# Firebase
> Backend, BaaS e banco · Status: **avaliado, não adotado** (alternativa ao Supabase quando o cliente pedir) · Revisado em 2026-10-30 · VTX-104

## 1. O que é
Plataforma de backend do Google: Auth, Cloud Firestore (NoSQL de documentos), Realtime Database, Cloud Storage, Cloud Functions, Hosting/App Hosting, Cloud Messaging (FCM, push), Crashlytics, Analytics e App Check. É serviço fechado; só os SDKs e a CLI `firebase-tools` são open source (MIT). O backend padrão da VTX continua o [Supabase](supabase.md) (VTX-023).

## 2. Quando usar / quando não usar
- **Usar:** cliente que já está no Firebase/Google Cloud; app mobile que precisa de push (FCM é grátis e é o caminho padrão no Android, ver [fluxo mobile](../../processos/fluxos/app-mobile.md)); Crashlytics e Analytics grátis.
- **Não usar:** dados relacionais e relatórios com SQL (Firestore não faz join); projeto que precisa de upload de arquivos sem cartão cadastrado (Storage exige Blaze); quem quer sair fácil do fornecedor (não há self-host).

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Supabase | padrão VTX | Postgres + RLS, região São Paulo, exporta SQL |
| [Appwrite](appwrite.md) | self-host | open source, Docker |
| Firebase só para FCM/Crashlytics | app com backend Supabase | produtos grátis no Spark, sem prender os dados |

## 4. Custo e plano gratuito (conferido em 30/10/2026)
- **Spark, US$ 0, sem cartão:** Firestore com 1 GiB armazenado, 50 mil leituras, 20 mil escritas e 20 mil exclusões **por dia** (zeram por volta da meia-noite do Pacífico) e 10 GiB/mês de saída; um banco grátis por projeto; Auth até 50 mil usuários ativos/mês (SMS cobrado à parte e só no Blaze); FCM, Crashlytics e Analytics sem custo. Ao estourar a cota, o produto para até o próximo ciclo.
- **Exige Blaze (pago por uso):** Cloud Storage (inclusive o bucket padrão, desde 03/02/2026; no Spark as chamadas dão 402/403), Cloud Functions (2 milhões de invocações/mês grátis) e App Hosting. O Blaze mantém as cotas grátis, mas exige cartão e não tem teto: alerta de orçamento só avisa.
- **Qualquer projeto no Blaze é decisão do Samuel (A2)**, com alerta de orçamento configurado.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | backend | só se o cliente pedir; senão Supabase |
| [Mobile](../../processos/fluxos/app-mobile.md) | push e falhas | FCM + Crashlytics, mesmo com backend Supabase |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | demo | Spark sem Storage; cuidado com a cota diária |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | sistema herdado | manter; migrar só com ADR e exportação testada |

## 6. Papel responsável
Arquiteto decide por ADR (modelo de documentos e regras); Dev Backend escreve Security Rules e Functions; Dev Frontend/Mobile integra SDK, FCM e App Check; DevOps cuida de projetos `dev`/`prod`, chaves e orçamento; QA testa as regras no emulador; Samuel aprova Blaze ([papéis](../../../agents/)).

## 7. Setup
1. Local primeiro: `firebase-tools` + **Emulator Suite** (Auth, Firestore, Functions, Storage) para desenvolver e testar regras sem tocar a nuvem nem gastar cota.
2. Dois projetos (`dev` e `prod`); Firestore em `southamerica-east1` (São Paulo). A região não muda depois.
3. Regras e índices versionados (`firestore.rules`, `storage.rules`, `firestore.indexes.json`) e publicados pelo CI com `firebase deploy --only`.
4. **MCP:** a CLI tem servidor MCP (`firebase mcp`); usar só no projeto `dev`.

## 8. Segredos e segurança/LGPD
- A chave de API web do Firebase não é segredo (identifica o projeto); a proteção são as **Security Rules** e o **App Check**. Nunca publicar regra aberta (`if true`) nem deixar o "modo de teste" vencer em produção.
- Conta de serviço (Admin SDK) só no servidor/CI como segredo; nunca no app nem no repositório.
- Dado pessoal: Firestore em São Paulo; Analytics e Crashlytics coletam dados do aparelho e entram na política de privacidade e no consentimento ([desenvolvimento seguro](../../seguranca/desenvolvimento-seguro.md)).

## 9. Checklist
- [ ] ADR justificando Firebase em vez de Supabase (ou só FCM/Crashlytics)
- [ ] Projetos `dev` e `prod`; região `southamerica-east1`
- [ ] Rules versionadas e testadas no emulador com dois usuários (QA)
- [ ] App Check ligado em produção
- [ ] Blaze só com aprovação do Samuel e alerta de orçamento
- [ ] Exportação dos dados testada (saída do fornecedor)

## 10. Registro de avaliação e Fontes
**ADR curto (30/10/2026):** *Contexto:* catálogo F12; Supabase já adotado. *Opções:* adotar como padrão, manter como alternativa, descartar. *Decisão:* alternativa quando o cliente pedir; FCM e Crashlytics podem ser usados em apps mesmo com backend Supabase. *Consequência:* sem custo no Spark; Storage e Functions dependem de A2.
- Preços: https://firebase.google.com/pricing
- Planos Spark e Blaze: https://firebase.google.com/docs/projects/billing/firebase-pricing-plans
- Cotas do Firestore: https://firebase.google.com/docs/firestore/quotas
- Storage exige Blaze: https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024
- Regiões do Firestore: https://firebase.google.com/docs/firestore/locations
- Security Rules: https://firebase.google.com/docs/rules
- App Check: https://firebase.google.com/docs/app-check
- Chaves de API: https://firebase.google.com/docs/projects/api-keys
- Emulator Suite: https://firebase.google.com/docs/emulator-suite
- MCP: https://firebase.google.com/docs/cli/mcp-server
