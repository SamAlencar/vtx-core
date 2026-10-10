# VTX — Empresa de TI operada por agentes de IA

A **VTX** é uma empresa de desenvolvimento de sistemas, aplicativos e plataformas operada por agentes de IA, sob supervisão humana (Samuel).
Este repositório **privado** concentra o código, a base de conhecimento técnico e o backlog da empresa.

## Arquitetura

| Componente | Onde | Função |
|---|---|---|
| `vtx-core` (este repositório, privado) | GitHub | Código, base de conhecimento, definições de agentes, backlog diário |
| `vtx_painel` (público) | GitHub Pages | Painel de acompanhamento gerado automaticamente a partir do backlog (apenas dados sanitizados) |
| Pasta "VTX - Empresa de Agentes IA" | Google Drive (conta VTX) | Gestão, projetos, documentos e relatórios |

Fluxo: `backlog/AAAA-MM-DD.yaml` → GitHub Action `sincronizar-painel` → `vtx_painel/data/backlog.json` → GitHub Pages.
A exportação leva **somente** `data`, `titulo`, `area` e `status`. Notas, responsáveis, caminhos e código nunca saem deste repositório.

## Estrutura

```
knowledge/        Base de conhecimento (um tema por arquivo Markdown curto)
  INDEX.md        Índice de todos os documentos
  ROADMAP.md      Próximos temas a pesquisar, em ordem de prioridade
agents/           Definições dos papéis de agentes (a preencher)
backlog/          Backlog mestre (projeto.yaml) + diário (AAAA-MM-DD.yaml) + SCHEMA.md
projects/         Projetos de clientes / produtos (um subdiretório por projeto)
scripts/          Exportação sanitizada para o painel e próxima tarefa (proxima_tarefa.py)
.github/workflows Sincronização automática do painel (ativa)
```

## Princípio de economia de tokens

A base de conhecimento cresce **incrementalmente**: um tema por sessão, cada documento curto e autocontido
(conceitos → metodologia → exemplos → checklist, com fontes). Os agentes consultam o `INDEX.md` e carregam
apenas o documento necessário para a tarefa.

## Convenções

- Idioma: português (pt-BR).
- Todo trabalho do dia é registrado em `backlog/AAAA-MM-DD.yaml` seguindo `backlog/SCHEMA.md`.
- Documentos de conhecimento citam fontes com links.
