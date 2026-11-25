# Fluxo de projeto: app mobile

> VTX-068 · Fase F1 · Base de Conhecimento. Especializa o [SOP entre agentes](../fluxo-entre-agentes.md) para aplicativos instalados no celular. Vale quando a [triagem](triagem.md) define `tipo_principal: app-mobile`.

## 1. Conceitos
- **App mobile:** aplicativo instalado no Android ou iOS e publicado na Play Store ou App Store. A entrega passa por revisão da loja, assinatura do binário e recursos do aparelho (câmera, GPS, push, uso sem rede).
- **Stack (ADR):** nativo (Kotlin e Swift), **Flutter** (Dart, UI própria), **React Native** (JavaScript/TypeScript, UI nativa) ou **Kotlin Multiplatform** (lógica compartilhada; UI nativa ou Compose). Pesam o time, os plugins e o prazo de loja.
- **Contrato primeiro:** o backend entra por OpenAPI, para o app e a API andarem em paralelo. Se a API for entrega própria, é módulo [API e integrações](api-integracoes.md). O incremento é uma fatia (tela + integração + teste no aparelho) numa trilha de teste.
- **Ferramentas:** padrão — GitHub Actions, Cursor, Supabase, Stripe, Sentry, Figma. Expo/EAS só se o ADR escolher React Native; Firebase pode entrar só para FCM/Crashlytics. Detalhe na [matriz ferramenta × fluxo](../../ferramentas/README.md#matriz); a escolha formal fica no [stack de referência](../../tecnologia/stack-de-referencia.md) e no ADR.

## 2. Etapas do fluxo

| # | Etapa | Papéis | Artefatos | Portão |
|---|---|---|---|---|
| 0 | Triagem | Orquestrador | `projects/<p>/ficha.yaml` | `tipo_principal: app-mobile` |
| 1 | Descoberta e requisitos | Produto (+ UX) | PRD, plataformas, histórias, offline e permissões | **Samuel aprova escopo e MVP** |
| 2 | UX/UI | UX/UI Designer | Fluxos, protótipo, WCAG 2.2 AA | Produto valida contra histórias |
| 3 | Arquitetura | Arquiteto (+ Segurança) | ADR de stack, OpenAPI, sync, deep links e push | Revisão do Orquestrador; Segurança se houver dado pessoal |
| 4 | Fundação | DevOps + Dev Frontend/Mobile (+ Backend) | CI, assinatura no CI, trilhas de teste, esqueleto e mock | Build na trilha interna |
| 5 | Incrementos | Dev Frontend/Mobile + Backend + QA | PRs com teste em emulador e aparelho real | CI verde, aceite, revisão independente |
| 6 | Endurecimento | QA + Segurança | E2E, MASVS L1, permissões, offline, deep link, acessibilidade | Sem falha crítica ou alta aberta |
| 7 | Lançamento | DevOps + Orquestrador | Ficha da loja, política de privacidade, notas, submissão | **Samuel aprova a submissão** |
| 8 | Operação e evolução | DevOps + Produto | Crashes e versões; demandas novas em [manutenção](manutencao-evolucao.md) | Retrospectiva registrada |

As etapas 5 e 6 repetem por incremento, publicado na trilha interna (Play *internal testing* ou TestFlight interno).

## 3. Pontos de aprovação do Samuel
1. Escopo, plataformas e corte do MVP (etapa 1).
2. ADR de stack e contas pagas de desenvolvedor (Apple e Google), na etapa 3.
3. Permissões sensíveis (câmera, localização, inclusive em segundo plano) e dados pessoais (LGPD), na etapa 3, com Segurança.
4. Cada submissão às lojas e a publicação em produção (etapa 7). A revisão é assíncrona e pode recusar.

## 4. Itens específicos de mobile
- **Assinatura e segredos:** Play App Signing guarda a chave de distribuição; a chave de upload fica só no CI. No iOS, certificado, *provisioning profile* e chave da API do App Store Connect também só no CI. Perder chave ou certificado atrasa a atualização até a recuperação com a loja.
- **Teste e revisão:** trilha *internal* da Play e TestFlight interno (até 100 testadores cada) antes do teste externo ou fechado. O primeiro build externo do TestFlight passa por revisão beta. Publicação gerenciada na Play evita ir ao ar no instante da aprovação.
- **Push:** FCM no Android e APNs no iOS (o FCM pode encaminhar). No iOS o usuário autoriza. O app registra o token; o backend envia.
- **Offline e sync:** leitura no banco local; escritas numa fila. O conflito (servidor ganha ou última escrita) é ADR. Retentativa exige operação idempotente no contrato.
- **Deep links:** HTTPS verificado — App Links (`assetlinks.json`) e Universal Links (`apple-app-site-association`). Esquema customizado só como reserva.
- **Permissões e acessibilidade:** câmera e localização no momento do uso, com texto de propósito; o app segue se o usuário negar. Localização em segundo plano exige declaração na loja e aprovação do Samuel. WCAG 2.2 AA: contraste, rótulos (TalkBack/VoiceOver), alvo de toque, sem depender só da cor.

## 5. Riscos típicos e mitigação

| Risco | Mitigação |
|---|---|
| Loja recusa por permissão, privacidade ou metadados | Permissões no PRD, política de privacidade, ensaio na trilha de teste |
| Revisão atrasa o lançamento | Folga na submissão; rejeição vira issue, sem crescer o escopo |
| Chave de assinatura perdida ou vazada | Segredos só no CI; Play App Signing; recuperação com DevOps |
| Plugin não cobre câmera, push ou offline | Prova na etapa 4; ADR registra ponte nativa ou troca de stack |
| Conflito de dados offline | Estratégia no ADR, API idempotente, teste sem rede |
| Defeito que só aparece no aparelho | Um aparelho real por plataforma no checklist de QA |

## 6. Exemplo
"App de pedidos no salão, Android e iOS, sem rede." Etapa 1: MVP = cardápio + pedido offline; Samuel aprova as duas lojas. Etapa 3: ADR-001 Flutter; OpenAPI idempotente; conflito "servidor ganha". Etapa 4: segredos no CI; builds no *internal* e no TestFlight interno. Etapa 5: 3 incrementos (cardápio, pedido, push de status). Etapa 6: teste sem rede acha pedido duplicado; corrigido no contrato. Etapa 7: Samuel aprova a submissão; a revisão aceita e a publicação gerenciada espera o ok final.

## 7. Checklist de conclusão
- [ ] PRD com plataformas, offline e permissões; MVP aprovado pelo Samuel
- [ ] ADR de stack, OpenAPI, sync, deep links e push salvos
- [ ] Assinatura só no CI; build no *internal* e no TestFlight interno
- [ ] Jornadas críticas em aparelho real, inclusive sem rede
- [ ] MASVS L1 verificado; sem falha crítica ou alta
- [ ] WCAG 2.2 AA nas telas principais (TalkBack ou VoiceOver)
- [ ] Ficha da loja e política de privacidade prontas; submissão aprovada pelo Samuel
- [ ] Notas de versão e retrospectiva registradas


## Recursos por papel
Áreas deste fluxo: frontend e design, backend e APIs, testes e QA, MCP. Fonte: [recursos.yaml](../../ferramentas/recursos.yaml) (narrativa em [bibliotecas-e-recursos.md](../../ferramentas/bibliotecas-e-recursos.md)). Usar só o que está **adotado**, listado nas seções dos agentes [Frontend/Mobile](../../../agents/dev-frontend-mobile.md), [Backend](../../../agents/dev-backend.md), [QA](../../../agents/qa.md). Em avaliação não entra no incremento sem piloto. Se esta página e o YAML divergirem, vale o YAML.

## Fontes
- JetBrains, *What is cross-platform mobile development?* (nativo, Flutter, React Native, Kotlin Multiplatform): https://kotlinlang.org/docs/multiplatform/cross-platform-mobile-development.html
- Google, *Flutter*: https://docs.flutter.dev/ · Meta, *React Native*: https://reactnative.dev/
- Google, *Sign your app* (Play App Signing): https://developer.android.com/studio/publish/app-signing · *Use Play App Signing*: https://support.google.com/googleplay/android-developer/answer/9842756 · *Managed publishing*: https://support.google.com/googleplay/android-developer/answer/9859654
- Google, *Internal, closed, or open testing*: https://support.google.com/googleplay/android-developer/answer/9845334 · Apple, *TestFlight overview*: https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/ · *App Review Guidelines*: https://developer.apple.com/app-store/review/guidelines/
- Firebase, *Cloud Messaging*: https://firebase.google.com/docs/cloud-messaging · Android, *App Links*: https://developer.android.com/training/app-links/about · Apple, *Universal Links*: https://developer.apple.com/documentation/xcode/supporting-universal-links-in-your-app
- Android, *Offline-first*: https://developer.android.com/topic/architecture/data-layer/offline-first · *Permissions*: https://developer.android.com/guide/topics/permissions/overview
- OWASP, *MASVS*: https://mas.owasp.org/MASVS/ · W3C, *WCAG 2.2*: https://www.w3.org/TR/WCAG22/ · *Mobile Accessibility*: https://www.w3.org/WAI/standards-guidelines/mobile/
- OpenAPI Initiative, *OpenAPI Specification*: https://spec.openapis.org/oas/latest.html · Brasil, Lei nº 13.709/2018 (LGPD): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
