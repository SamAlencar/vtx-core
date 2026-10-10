# Formato do Backlog Diário

Um arquivo por dia: `backlog/AAAA-MM-DD.yaml`.

```yaml
data: "2026-10-10"          # obrigatório, AAAA-MM-DD (igual ao nome do arquivo)
tarefas:
  - id: VTX-001             # obrigatório, único e sequencial no projeto
    titulo: "Texto curto"   # obrigatório — PÚBLICO (vai para o painel)
    area: "Infraestrutura"  # obrigatório — PÚBLICO
    status: "concluído"     # obrigatório — PÚBLICO: "a fazer" | "em andamento" | "concluído"
    responsavel: "agente-x" # obrigatório — PRIVADO
    notas: "detalhes"       # opcional — PRIVADO
```

## Áreas sugeridas
Infraestrutura, Organização, Base de Conhecimento, Produto, Arquitetura, Desenvolvimento, Qualidade, Segurança, DevOps, Gestão.

## Regras
- Uma tarefa que continua no dia seguinte é repetida no novo arquivo com o mesmo `id` e o status atualizado.
- **Nunca** colocar dados sensíveis em `titulo` ou `area`: esses campos são publicados no painel público.
- Apenas `data`, `id`, `titulo`, `area` e `status` são exportados por `scripts/exportar_painel.py`.
