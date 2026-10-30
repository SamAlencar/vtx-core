# Expo e EAS
> Mobile · Status: **recomendado quando o ADR escolher React Native** (Free + build local) · Revisado em 2026-10-30 · VTX-105

## 1. O que é
**Expo** é o framework open source (MIT, SDK 58 de 14/10/2026) sobre React Native: CLI, Expo Router, módulos nativos (câmera, push, arquivos) e *prebuild*, que gera os projetos Android/iOS a partir do `app.json`/`app.config.ts`. **EAS** (Expo Application Services) é a nuvem paga por uso da Expo: Build (gera APK/AAB/IPA), Submit (envia às lojas), Update (atualização OTA de JS e assets) e Workflows (CI).

## 2. Quando usar / quando não usar
- **Usar:** o ADR do [fluxo mobile](../../processos/fluxos/app-mobile.md) escolheu React Native; time em TypeScript que reaproveita código e componentes do web; iOS sem ter Mac para o build (EAS Build).
- **Não usar:** ADR escolheu Flutter, nativo ou Kotlin Multiplatform; app com SDK nativo raro sem módulo (avaliar *config plugin* na prova da etapa 4 antes).

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Expo + build local (`eas build --local`) | padrão VTX sem custo | não consome cota; iOS exige macOS com Xcode |
| Expo + EAS Build Free | sem Mac para iOS | 15 Android + 15 iOS por mês, fila lenta |
| React Native puro (CLI) | projeto herdado | mais configuração nativa manual |
| Flutter / nativo | ADR de stack | ver fluxo mobile |

## 4. Custo e plano gratuito (conferido em 30/10/2026)
- **Free, US$ 0:** até 15 builds Android e 15 iOS por mês em fila de baixa prioridade (pode passar de 90 min no pico; limite de 45 min por build); Submit às lojas; updates ilimitados para até 1.000 usuários ativos/mês (MAU) e 100 GiB de banda; 60 min de Workflows. **Sem cobrança de excedente:** acabou a cota, builds na nuvem param até o dia 1º; o caminho é build local.
- **Pagos:** Starter US$ 19/mês e Production US$ 199/mês, mais uso. Assinatura de código dos updates só no Production; ferramentas de servidor do MCP da Expo exigem plano pago.
- **Fora da Expo:** contas de desenvolvedor Apple (anual) e Google Play (taxa única) são obrigatórias para publicar. **Plano pago do EAS e contas de loja são decisões do Samuel (A2)**, já previstas na etapa 3 do fluxo mobile.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [Mobile](../../processos/fluxos/app-mobile.md) | 3–7 | stack RN, build, teste interno (TestFlight/trilha interna), Submit e Update |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | demo | Expo Go ou build de desenvolvimento, sem loja |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | correção | Update OTA para bug só de JS; mudança nativa = nova versão na loja |

## 6. Papel responsável
Arquiteto registra no ADR (Expo, SDK, OTA sim/não); Dev Frontend/Mobile mantém o app, `app.config.ts` e `eas.json`; DevOps cuida de credenciais de assinatura, perfis de build, canais de update e CI; QA testa no aparelho real e na trilha interna; Samuel aprova submissão, contas de loja e plano pago ([papéis](../../../agents/)).

## 7. Setup
1. `npx create-expo-app` com TypeScript e Expo Router; versão do SDK fixada; `npx expo install` para manter dependências compatíveis.
2. `eas.json` com perfis `development`, `preview` (interno) e `production`; `runtimeVersion` pela política `fingerprint` para um update nunca cair em binário incompatível.
3. Build local (`eas build --local`) no Linux para Android e em macOS para iOS; nuvem Free só quando faltar Mac.
4. Canais de update (`preview`, `production`); republicar em produção só após teste no canal `preview`.
5. **MCP:** usar só a parte de documentação; ferramentas de servidor são pagas.

## 8. Segredos e segurança/LGPD
- Variável `EXPO_PUBLIC_*` vai embutida no app: nunca segredo nela; chave de API real fica no backend.
- Chaves de assinatura (keystore, certificados, chave da API do App Store Connect) só nas credenciais do EAS ou no CI; nunca no repositório.
- Update OTA não pode mudar o propósito do app nem burlar a revisão das lojas; mudança de permissão ou nativa sai como versão nova.
- Permissões com texto de propósito e política de privacidade ([desenvolvimento seguro](../../seguranca/desenvolvimento-seguro.md)).

## 9. Checklist
- [ ] ADR de stack cita Expo, SDK e uso de OTA
- [ ] `eas.json` com perfis e `runtimeVersion` por fingerprint
- [ ] Nenhum segredo em `EXPO_PUBLIC_*` nem no repositório
- [ ] Build local funcionando; cota do Free acompanhada
- [ ] Teste em aparelho real e trilha interna antes da submissão
- [ ] Submissão e contas de loja aprovadas pelo Samuel

## 10. Registro de avaliação e Fontes
**ADR curto (30/10/2026):** *Contexto:* catálogo F12; fluxo mobile deixa a stack para ADR. *Opções:* adotar Expo para todo RN, adotar com EAS pago, descartar. *Decisão:* Expo é o padrão quando a stack for React Native, com build local e EAS Free. *Consequência:* sem custo; build iOS na nuvem limitado à cota; plano pago só por A2.
- Preços: https://expo.dev/pricing
- Cota e excedentes do Free: https://docs.expo.dev/billing/faq/
- Build local: https://docs.expo.dev/build-reference/local-builds/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
- Assinatura de updates: https://docs.expo.dev/eas-update/code-signing/
- Variáveis de ambiente: https://docs.expo.dev/eas/environment-variables/
- Workflows: https://docs.expo.dev/eas/workflows/introduction/
- MCP: https://docs.expo.dev/eas/ai/mcp/
