# Formato do Backlog

Dois tipos de arquivo:

## 1. Backlog mestre — `backlog/projeto.yaml` (plano completo)

```yaml
projeto: "Nome do projeto"
fases:
  - {id: F1, nome: "Processo e operação de agentes"}
tarefas:
  - id: VTX-010            # único, estável, nunca reutilizado
    titulo: "Texto curto"  # PÚBLICO
    fase: F1               # PÚBLICO
    area: "Base de Conhecimento"  # PÚBLICO
    prioridade: 10         # PÚBLICO — menor = antes (ordem de execução)
    status: "a fazer"      # PÚBLICO — valor base
    entregavel: "knowledge/..."   # PRIVADO
```

## 2. Diário — `backlog/AAAA-MM-DD.yaml` (o que foi feito no dia)

```yaml
data: "2026-10-10"
tarefas:
  - id: VTX-010
    titulo: "Texto curto"   # PÚBLICO
    area: "Base de Conhecimento"  # PÚBLICO
    status: "concluído"     # PÚBLICO: "a fazer" | "em andamento" | "concluído"
    responsavel: "agente-x" # PRIVADO
    notas: "detalhes"       # PRIVADO
```

## Regras
- **Status efetivo** de uma tarefa = o do diário mais recente que cita o id; se nenhum cita, vale o do mestre.
- Tarefas novas entram primeiro no mestre (com id, fase e prioridade); depois são citadas nos diários.
- Campos opcionais PRIVADOS no mestre: `depende_de` (lista de ids) e `notas`.
- A ordem de execução é a `prioridade`, não o id (ex.: F9 vem antes de F8). A ordem das fases no painel segue a lista `fases`.
- Após editar o mestre, rodar `python scripts/gerar_roadmap.py` para atualizar `knowledge/ROADMAP.md`.
- `titulo`, `area` e `fase` são publicados no painel: **nunca** colocar dados sensíveis neles.
- Exportado por `scripts/exportar_painel.py`: projeto (id, titulo, fase, area, prioridade, status) e diários (data, id, titulo, area, status).

## Rotina diária
1. `python scripts/proxima_tarefa.py` → mostra a tarefa em andamento ou a próxima "a fazer" de menor prioridade.
2. Executar a tarefa (um documento por sessão) e atualizar `knowledge/INDEX.md`.
3. Criar/atualizar `backlog/AAAA-MM-DD.yaml` citando o id com o novo status e fazer push → o painel atualiza sozinho.
