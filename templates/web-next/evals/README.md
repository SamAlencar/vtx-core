# evals

Suíte mínima de evals do template (`npm run evals`).

- Casos em `datasets/*.jsonl`: feliz, recusa, erro de tool, argumento inválido e injeção de prompt (20 no total).
- Métricas: acerto de tool, validade do schema, recusa correta e número médio de passos, com limiar em `limiares.json`.
- Por padrão usa respostas gravadas (`modeloGravado`) e o domínio real. Sem rede e sem chave.
- Modelo real só fora do CI e com A2, e só depois de autenticação e limite de taxa na rota (follow-up da VTX-211).
- O comando gera `resultado.json` e sai com código 0 se todos os casos e os limiares passam. Um limiar acima do resultado faz o comando sair com código diferente de 0.

No CI do projeto gerado, o job `web` de `.github/workflows/ci.yml` roda `npm run evals`.
