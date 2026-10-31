# Docker
> CI/CD e infraestrutura · Status: **recomendado** (Engine/Compose para dev local, CI e saída VPS; Desktop só onde a licença permite) · Revisado em 2026-10-31 · VTX-109

## 1. O que é
Plataforma de contêineres: empacota app e dependências numa imagem que roda igual na máquina, no CI e no servidor. O Docker Engine (projeto Moby, v29.9.2) e o Compose (v5.6.1) são Apache-2.0. O Docker Desktop (interface para macOS/Windows) tem licença própria. É a base do `supabase start` ([DevOps/SRE](../../operacao/devops-sre.md)), do `act` ([GitHub Actions](github-actions.md)) e do self-host de [Supabase](../backend/supabase.md), [Appwrite](../backend/appwrite.md) e GlitchTip ([Sentry](../observabilidade/sentry.md)).

## 2. Quando usar / quando não usar
- **Usar:** ambiente local reproduzível (banco, fila, serviços) com `compose.yaml`; testes de integração no CI; backend longo em VPS; motores externos isolados ([competências](../../tecnologia/competencias-especializadas.md)).
- **Não usar:** para o que a hospedagem gerenciada já faz (Next.js na [Vercel](../hospedagem/vercel.md) ou [Cloudflare](cloudflare.md)); Kubernetes em projeto pequeno (YAGNI; k3s só com necessidade real e A2).

## 3. Alternativas
| Opção | Quando | Motivo |
|---|---|---|
| Docker Engine + Compose (Linux) | padrão | open source, sem restrição de licença |
| Colima (MIT) | macOS sem Desktop | roda Engine numa VM leve |
| Podman (Apache-2.0, v6.1.4) | sem daemon/root, Fedora/RHEL | compatível com CLI e Compose |
| Docker Desktop | dev em macOS/Windows | grátis só nas condições do §4 |

## 4. Custo e plano gratuito (conferido em 31/10/2026)
- **Engine, CLI, Compose, Buildx:** grátis e Apache-2.0.
- **Docker Desktop:** grátis para uso pessoal, ensino, open source não comercial e empresa com **menos de 250 funcionários e menos de US$ 10 mi/ano**. VTX e Tekto se enquadram hoje; cliente grande que fornece máquina deve ter licença própria. Assinatura é A2.
- **Docker Hub:** sem login, 100 pulls a cada 6 h por IP; Personal com login, 200 a cada 6 h; erro 429 ao estourar. Personal tem 1 repositório privado.
- **GHCR (GitHub Container Registry):** grátis para imagens públicas; privadas usam a cota de armazenamento e transferência da conta GitHub.

## 5. Nos fluxos
| Fluxo | Etapa | Uso |
|---|---|---|
| [SaaS](../../processos/fluxos/sistema-web-saas.md) | dev e CI | `compose.yaml` com Postgres/Supabase local; testes de integração |
| [API](../../processos/fluxos/api-integracoes.md) | dev, CI e produção | imagem do serviço; VPS quando precisar processo longo |
| [Manutenção](../../processos/fluxos/manutencao-evolucao.md) | onboarding | subir sistema legado do cliente sem instalar nada na máquina |
| [MVP/PoC](../../processos/fluxos/mvp-poc.md) | demonstração | opcional, para motor externo isolado |

## 6. Papel responsável
DevOps/SRE mantém Dockerfile, `compose.yaml`, registro e varredura; Devs usam localmente; Segurança revisa imagens base e varredura; Samuel aprova VPS, assinatura ou registro pago ([papéis](../../../agents/)).

## 7. Setup
1. Linux: Docker Engine pelo repositório oficial; macOS: Colima ou Desktop (se licença ok); Windows: WSL2 + Engine ou Desktop.
2. `compose.yaml` na raiz com serviços de dev e `.env.example`; `docker compose up -d` como único passo no README.
3. Dockerfile *multi-stage*, imagem base oficial e fixa (`node:22-slim`, por digest em produção), usuário não root, `.dockerignore` (sem `.env`, `.git`).
4. CI: `docker/login-action` no GHCR com `GITHUB_TOKEN` (evita o limite do Hub), build com cache, `trivy image` (Apache-2.0, v0.76.1) bloqueando CRITICAL.
5. Tag da imagem = SHA do commit; `latest` nunca em produção.

## 8. Segredos e segurança/LGPD
- Nunca `ENV`/`ARG` com segredo nem `.env` copiado para a imagem; usar `--secret` do BuildKit e variáveis em tempo de execução.
- Contêiner sem `--privileged` e sem montar `/var/run/docker.sock` (dá root no host).
- Imagem pública não pode conter dado de cliente; volumes de banco local com dado fictício ([desenvolvimento seguro](../../seguranca/desenvolvimento-seguro.md)).

## 9. Checklist
- [ ] `compose.yaml` sobe o dev com um comando
- [ ] Dockerfile multi-stage, não root, base fixa, `.dockerignore`
- [ ] CI autenticado no registro (GHCR) e com cache
- [ ] Trivy sem CRITICAL
- [ ] Nenhum segredo nas camadas (`docker history` conferido)
- [ ] Licença do Desktop conferida para cada máquina

## 10. Registro de avaliação e Fontes
**ADR curto (31/10/2026):** *Contexto:* dev local e self-host dependem de contêineres; a licença do Desktop mudou em 2021. *Opções:* Docker Engine/Compose, Podman, Desktop. *Decisão:* Engine + Compose como padrão, GHCR como registro, Trivy no CI; Desktop só dentro da licença grátis; Podman/Colima como alternativa. *Consequência:* mesmo `compose.yaml` em qualquer máquina.
- Licença do Docker Desktop: https://docs.docker.com/subscription-billing/desktop-license
- Limites de pull do Docker Hub: https://docs.docker.com/docker-hub/usage/pulls
- Instalar o Engine: https://docs.docker.com/engine/install/
- Boas práticas de build: https://docs.docker.com/build/building/best-practices/
- Segredos no build: https://docs.docker.com/build/building/secrets/
- Moby (Apache-2.0): https://github.com/moby/moby
- Podman: https://podman.io/
- Colima: https://github.com/abiosoft/colima
- GitHub Packages (cobrança): https://docs.github.com/en/billing/concepts/product-billing/github-packages
- Trivy: https://trivy.dev/
