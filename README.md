# VTX — Empresa de TI operada por agentes de IA

A **VTX** é uma empresa de desenvolvimento de sistemas, aplicativos e plataformas operada por agentes de IA, sob supervisão humana (Samuel).
Este repositório **privado** concentra o código, a base de conhecimento técnico e o backlog da empresa.

## Arquitetura

| Componente | Onde | Função |
|---|---|---|
| `vtx-core` (este repositório, privado) | GitHub | Código, base de conhecimento, definições de agentes, backlog diário |
| [`painel-central`](https://github.com/SamAlencar/painel-central) (público) | [GitHub Pages](https://samalencar.github.io/painel-central/) | Painel de acompanhamento (Tekto, VTX, 4med.co, Dark Channel), com dados sanitizados |
| Pasta "VTX - Empresa de Agentes IA" | Google Drive (conta VTX) | Gestão, projetos, documentos e relatórios |

O painel público lê o backlog deste repositório pela API do GitHub e se atualiza no próprio `painel-central` (workflow `atualizar.yml`, a cada 30 min). Não há workflow no vtx-core publicando o painel. Campos visíveis: `id`, `titulo`, `fase`, `area`, `prioridade`, `status`. Notas, responsáveis, caminhos e código não saem daqui.

A plataforma privada de acompanhamento (`SamAlencar/vtx-acompanhamento`, F11) é um projeto à parte e ainda não substitui o painel público.

O repositório `vtx_painel` e o workflow `sincronizar-painel` (secret `PANEL_TOKEN`) foram aposentados em 24/11/2026 (VTX-171).

## Estrutura

```
knowledge/        Base de conhecimento (um tema por arquivo Markdown curto)
  INDEX.md        Índice de todos os documentos
  ROADMAP.md      Próximos temas a pesquisar, em ordem de prioridade
agents/           Definições dos 7 papéis do núcleo + especialistas
backlog/          Backlog mestre (projeto.yaml) + diário (AAAA-MM-DD.yaml) + SCHEMA.md
projects/         Projetos de clientes / produtos (um subdiretório por projeto)
scripts/          Scripts do backlog (proxima_tarefa, exportar_painel local, qualidade)
tests/            Testes dos scripts do backlog (unittest)
.github/workflows CI de testes e qualidade (`testes.yml`)
```

## Princípio de economia de tokens

A base de conhecimento cresce **incrementalmente**: um tema por sessão, cada documento curto e autocontido
(conceitos → metodologia → exemplos → checklist, com fontes). Os agentes consultam o `INDEX.md` e carregam
apenas o documento necessário para a tarefa.

## Convenções

- Idioma: português (pt-BR).
- Todo trabalho do dia é registrado em `backlog/AAAA-MM-DD.yaml` seguindo `backlog/SCHEMA.md`.
- Documentos de conhecimento citam fontes com links.
