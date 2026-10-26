# Desenvolvimento mobile

> VTX-027 · Fase F4 · Base de Conhecimento. Como o **Dev Frontend/Mobile** ([dev-frontend-mobile.md](../../agents/dev-frontend-mobile.md)) constrói apps sobre o [stack de referência](stack-de-referencia.md): **Expo (React Native) + TypeScript**, mesmos contratos Zod e Supabase da web ([frontend web](frontend-web.md), [design de APIs](design-de-apis.md)).

## 1. Conceitos
- **Precisa mesmo de app?** App de loja só se houver câmera/GPS em segundo plano, notificação push essencial, uso offline ou exigência do cliente. Senão, **PWA** (a web do Next.js instalável): uma base só, sem taxa de loja. Decisão em ADR do Arquiteto.
- **Expo:** React Native com ferramentas prontas; `expo-router` (rotas por arquivo, como no Next.js), módulos nativos via `npx expo install` (versões compatíveis com o SDK). Código nativo próprio só com ADR.
- **Dois tipos de atualização:** (a) **binário** na loja (EAS Build + revisão da Apple/Google, dias); (b) **OTA** com EAS Update (só JS/imagens, minutos). OTA nunca muda permissões nem código nativo; `runtimeVersion` impede mandar JS para um binário incompatível.
- **App antigo vive por meses:** o usuário não atualiza. A API só muda de forma **aditiva** e o app tem verificação de versão mínima ("atualize para continuar") para quebras inevitáveis.
- **Lojas e custo:** EAS Build/Update têm plano gratuito limitado; conta Apple Developer (anual) e Google Play (taxa única) são **custos A2** ([governança](../processos/governanca-e-aprovacoes.md)), contratados em nome do cliente.

## 2. Metodologia
1. **Telas do Figma em padrões nativos** (lei de Jakob): abas embaixo, voltar do sistema no Android, áreas seguras (`SafeAreaView`), alvo de toque ≥ 44×44 pt (Apple) / 48×48 dp (Android).
2. **Rede ruim é o normal:** estados carregando/erro/vazio, nova tentativa automática nas leituras, rascunho local de formulários (`expo-sqlite` ou AsyncStorage), envio idempotente com `Idempotency-Key`.
3. **Segredos e sessão:** `EXPO_PUBLIC_*` vai dentro do app e é **público** (qualquer um extrai); só URL e chave `anon` do Supabase. Token de sessão em `expo-secure-store`. Pagamento e regra sensível passam pelo servidor.
4. **Permissões no momento do uso**, com texto explicando o motivo (LGPD e revisão da loja); negar não pode travar o app.
5. **Acessibilidade:** `accessibilityLabel` em ícones, suporte a fonte grande do sistema, contraste AA, testar com TalkBack e VoiceOver.
6. **Testar:** Jest + React Native Testing Library nos componentes; fluxo principal em aparelho real Android barato (o público típico) e no simulador iOS; Maestro (open source) para E2E quando houver fluxo crítico.
7. **Publicar:** perfis `development`, `preview` (teste interno) e `production` no `eas.json`; produção e envio à loja só com aprovação ([DevOps e SRE](../operacao/devops-sre.md)).

## 3. Exemplo: `eas.json` mínimo
```json
{
  "cli": { "appVersionSource": "remote" },
  "build": {
    "development": { "developmentClient": true, "distribution": "internal" },
    "preview": { "distribution": "internal", "channel": "preview" },
    "production": { "channel": "production", "autoIncrement": true }
  }
}
```
Com `"runtimeVersion": { "policy": "fingerprint" }` no `app.json`, a mudança nativa gera nova runtime e o OTA antigo não chega a binário incompatível.

## 4. Checklist do PR mobile
- [ ] App de loja justificado em ADR (senão, PWA).
- [ ] Nenhum segredo em `EXPO_PUBLIC_*`; sessão no `expo-secure-store`.
- [ ] Estados de rede ruim e rascunho local do formulário testados com o modo avião.
- [ ] Mudança de API compatível com a versão anterior do app; versão mínima conferida.
- [ ] Mudança nativa = novo binário; OTA só para JS, com `runtimeVersion` correto.
- [ ] Testado em Android real e iOS; TalkBack/VoiceOver e fonte grande ok.
- [ ] Publicação na loja ou custo novo com aprovação A2.

## 5. Fontes
- Expo — documentação: https://docs.expo.dev/
- Expo Router: https://docs.expo.dev/router/introduction/
- EAS Update e runtime version: https://docs.expo.dev/eas-update/runtime-versions/
- Expo — variáveis de ambiente: https://docs.expo.dev/guides/environment-variables/
- Expo SecureStore: https://docs.expo.dev/versions/latest/sdk/securestore/
- React Native — acessibilidade: https://reactnative.dev/docs/accessibility
- Apple HIG — layout e alvos de toque: https://developer.apple.com/design/human-interface-guidelines/layout
- Android — acessibilidade (alvos 48dp): https://developer.android.com/guide/topics/ui/accessibility/apps
- Maestro: https://maestro.dev/
