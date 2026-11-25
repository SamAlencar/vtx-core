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
    status: "a fazer"      # PÚBLICO — valor base: a fazer | em andamento | concluído | aguardando | cancelado
    entregavel: "knowledge/..."   # PRIVADO
```

## 2. Diário — `backlog/AAAA-MM-DD.yaml` (o que foi feito no dia)

```yaml
data: "2026-10-10"
tarefas:
  - id: VTX-010
    titulo: "Texto curto"   # PÚBLICO
    area: "Base de Conhecimento"  # PÚBLICO
    status: "concluído"     # PÚBLICO: "a fazer" | "em andamento" | "concluído" | "aguardando" | "cancelado"
    responsavel: "agente-x" # PRIVADO
    notas: "detalhes"       # PRIVADO
```

## Regras
- **Status efetivo** de uma tarefa = o do diário mais recente que cita o id; se nenhum cita, vale o do mestre. Valores: `a fazer`, `em andamento`, `concluído`, `aguardando`, `cancelado`. Qualquer outro valor vira `a fazer`.
- **aguardando:** a tarefa existe, mas espera aprovação, dependência externa ou decisão do Samuel. Não entra na fila do `proxima_tarefa.py` e continua no denominador do progresso.
- **cancelado:** a tarefa saiu de escopo (ex.: VTX-142). Não entra na fila, não conta como concluída e é excluída do total do progresso e do roadmap.
- Tarefas novas entram primeiro no mestre (com id, fase e prioridade); depois são citadas nos diários.
- Campos opcionais PRIVADOS no mestre: `depende_de` (lista de ids) e `notas`.
- A ordem de execução é a `prioridade`, não o id (ex.: F9 vem antes de F8). A ordem das fases no painel segue a lista `fases`.
- Após editar o mestre, rodar `python scripts/gerar_roadmap.py` para atualizar `knowledge/ROADMAP.md`.
- `titulo`, `area` e `fase` aparecem no [painel público](https://samalencar.github.io/painel-central/): **nunca** colocar dados sensíveis neles.
- O painel público (`SamAlencar/painel-central`) lê o backlog pela API e se atualiza no próprio repositório. `scripts/exportar_painel.py` é um exportador local de campos sanitizados (projeto: id, titulo, fase, area, prioridade, status; diários: data, id, titulo, area, status); não publica o site.

## Rotina diária
1. `python scripts/proxima_tarefa.py` → mostra a tarefa em andamento ou a próxima "a fazer" de menor prioridade.
2. Executar a tarefa (um documento por sessão) e atualizar `knowledge/INDEX.md`.
3. Criar/atualizar `backlog/AAAA-MM-DD.yaml` citando o id com o novo status e fazer push. O [painel público](https://samalencar.github.io/painel-central/) reflete a mudança na próxima atualização dele (cerca de 30 min), não por um workflow deste repositório.
