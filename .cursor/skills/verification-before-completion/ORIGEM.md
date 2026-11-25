# Proveniência — verification-before-completion
- Repositório: https://github.com/obra/superpowers (path skills/verification-before-completion)
- Commit fixado: bb92a77741419a4ab5f06e711a283343f1ada0c3 (2026-10-09)
- Licença: MIT (Jesse Vincent) — cópia em LICENSE
- Revisado em: 2026-10-18 por Tek
- O que faz: Proíbe declarar 'pronto' sem rodar o comando de verificação e ler a saída.
- Encaixe no fluxo do Tek: Antes de dizer que o CI está verde, mesclar ou atualizar logs.
- Riscos verificados: sem chamadas de rede, sem instalação de pacotes, sem acesso a credenciais, sem instrução para burlar checks. 
- Ajustes para regras Tekto: docs/respostas em pt-BR; nunca tocar .github/workflows; uma tarefa por execução; PR só com CI verde e squash-merge. Evidência = pytest local + checks do PR verdes.

## Edições aplicadas (2026-10-18)
Originais em `orig/` (diff: `diff -ru orig/ .`).
- Adicionada seção "Regras Tekto" ao fim do SKILL.md (pt-BR, nunca `.github/workflows`, uma tarefa por execução).

> VTX: copiado do original (orig/) revisado pelo Tek; obra/superpowers @ bb92a77, MIT. Na VTX, verificar = rodar tests/ e confirmar o workflow testes.yml (jobs unittest e qualidade) antes de marcar concluído.
