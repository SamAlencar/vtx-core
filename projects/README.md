# Projetos

Política: [isolamento por cliente](../knowledge/seguranca/isolamento-clientes.md) (VTX-175). Cada cliente tem repositório próprio, gerado por `scripts/bootstrap_projeto.sh`. Neste diretório o vtx-core guarda **só ponteiro e metadados públicos**. Código, dados e segredos não entram aqui.

## Ponteiros e legado

- [plataforma-projetos](plataforma-projetos/) — piloto da plataforma de projetos (VTX). Documentação ainda neste repositório (legado, a migrar). Sem código de produto nem segredo.
- [med-hub](med-hub/) — 4med.co, em paralelo ao piloto (20/10/2026). PRD e ADRs ainda neste repositório (legado, a migrar para o repositório do produto). Sem código de aplicativo nem segredo.
- [sandbox-impeccable](sandbox-impeccable/) — piloto da skill/detector Impeccable (VTX-127); é sandbox de ferramenta da VTX, não repositório de cliente.

## Na fila (fluxo site/landing page, depois do piloto e do med-hub; ordem a confirmar)

Repositórios próprios, quando existirem — não pastas novas de código neste `projects/`:

- site-vtx — base em [SamAlencar/vtx-systems-site](https://github.com/SamAlencar/vtx-systems-site) (Next.js, parcial, 03/2026); hospedagem gratuita.
- site-med-hub — base em [SamAlencar/4medco-website](https://github.com/SamAlencar/4medco-website) (Vite + React + Tailwind, 12/2025).
- site-tekto — parcialmente iniciado; repositório ainda não localizado (aguardando o Samuel indicar).
