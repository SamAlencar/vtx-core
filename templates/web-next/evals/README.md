# evals

Suíte mínima de evals do template (`npm run evals`).

- Casos em `datasets/*.jsonl`: feliz, recusa, erro de tool, argumento inválido e injeção de prompt (20 no total).
- Métricas: acerto de tool, validade do schema, recusa correta e número médio de passos, com limiar em `limiares.json`.
- A suíte usa só respostas gravadas (`modeloGravado`) e o domínio real. Sem rede, sem chave e sem modo de modelo real neste runner. Um modo com modelo real fica para tarefa futura (A2, dependência da VTX-226).
- Os casos de `recusa` e `injecao` validam o harness e o contrato (o roteiro gravado já responde `{"recusa":true}` e a métrica `recusa_correta` confere que o harness não inventa chamada de tool). Não medem o comportamento de um modelo nem a defesa contra injeção no prompt.
- O comando gera `resultado.json` e sai com código 0 se todos os casos e os limiares passam. Um limiar acima do resultado faz o comando sair com código diferente de 0.

O job `web` de `.github/workflows/ci.yml` (projeto gerado) e o job `web-next` do CI do vtx-core rodam `npm run evals`.
