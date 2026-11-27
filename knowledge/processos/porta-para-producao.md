# Porta para produção: CI com autofix, revisão cruzada e revisão humana por risco

> VTX-222 · Fase F1 · Processo. O caminho que um PR percorre até o merge (e, em projeto de cliente, até produção), com o peso da revisão proporcional ao risco. Vale para o vtx-core e para os repositórios de cliente. Regra geral de aprovação: [governança](governanca-e-aprovacoes.md). Topologia de quem revisa: [topologia-de-agentes.md](topologia-de-agentes.md).

## 1. Três portões, nesta ordem

1. **CI verde** com autofix do próprio agente (§2).
2. **Revisão cruzada por IA** com contexto limpo e veredito na HEAD exata (§3).
3. **Revisão humana calibrada por risco**, mais smoke test em staging quando a classe pede (§4).

O repositório privado no plano gratuito do GitHub não tem proteção de branch, então a plataforma não bloqueia merge com CI vermelho. O caminho previsto é `scripts/mesclar_pr.sh <n>` (VTX-214): o script confere os checks (`gh pr checks --json name,state,bucket`) e o veredito na HEAD exata e só então chama `gh pr merge <n> --squash --match-head-commit <sha>`. Não use `gh pr merge` direto.

Limitações do portão, nesta versão:

- Sys (autor) e Tzu (revisor) publicam com a mesma conta GitHub (`SamAlencar`). Filtrar o comentário por `user.login` não autentica o revisor. O script só aceita o formato do revisor, com a HEAD exata na primeira linha: `**Veredito: <texto>** (HEAD \`<sha>\`)`. O autor nunca escreve linha de Veredito. Separar a identidade do revisor (conta própria ou GitHub App) é a [VTX-227](../../backlog/projeto.yaml).
- O caráter sensível depende só da etiqueta "precisa do Samuel" no momento do merge. Se ela for removida, o script passa a exigir apenas **Aprovado**.

## 2. CI com autofix

- Antes de abrir o PR, o agente roda localmente o que o CI roda. No vtx-core: `pip install -e ".[dev]"`, `ruff check --fix core scripts tests`, `mypy core/vtx_ifc`, `python -m unittest discover -s tests`, `python scripts/validar_backlog.py`, `python scripts/verificar_links.py`. O CI só verifica (`ruff check` e `mypy`, sem `--fix`).
- CI vermelho: quem abriu o PR lê o log (`gh run view <id> --log-failed`), corrige na mesma branch e espera de novo. Até **3 tentativas**; na quarta, para, registra no PR o que tentou e escala ao orquestrador.
- O autofix é feito pelo agente, não por um bot de CI com permissão de escrita (isso seria `contents: write` no workflow, mudança sensível).
- Nunca "consertar" CI apagando teste, baixando limiar ou pulando check. Se o teste estiver errado, isso vai explícito na descrição do PR.

## 3. Revisão cruzada por IA

- O revisor é outra sessão, com **contexto limpo** (lê o diff, a descrição e os documentos citados, não a conversa de quem escreveu) e, quando o plano oferecer, **modelo diferente** do autor ([topologia §4](topologia-de-agentes.md)).
- O veredito fica escrito no PR, com a HEAD revisada: **Aprovado**, **Aprovado com ressalvas** ou **Mudanças necessárias**, e a lista de achados com arquivo e linha.
- O veredito vale para aquele commit. Push novo (inclusive rebase) pede veredito novo.
- **Aprovado com ressalvas:** o autor aplica as ressalvas que o revisor marcou como "corrigir antes do merge", registra no PR o que mudou e pede veredito novo na HEAD final. O merge só acontece com veredito **Aprovado** do revisor de IA nessa HEAD final (ou **Aprovado (aval do Samuel delegado ao Tzu)** quando o PR tem a etiqueta). **Aprovado com ressalvas** na HEAD de merge não libera. O autor (Sys) não pede aprovação ao Samuel; o revisor de IA pode consultar a opinião dele antes de dar o aval. Em PR com a etiqueta "precisa do Samuel", o veredito na HEAD final precisa ser **Aprovado (aval do Samuel delegado ao Tzu)** (além do CI verde). O aval delegado ao Tzu cobre o merge de PRs e mudanças de permissões, acessos e ferramentas de agente no repositório; não cobre deploy em produção, dinheiro e gasto, comunicação externa/clientes nem dados pessoais, que pertencem ao Samuel (regra definitiva). Ressalva não bloqueante vira tarefa de acompanhamento.
- Autor e revisor nunca são a mesma sessão. Aprovar o próprio trabalho é A3.

## 4. Classes de risco

| Classe | Exemplos | Portões para o merge | Antes de produção (cliente) |
|---|---|---|---|
| **Trivial** | Erro de digitação, status de backlog, ROADMAP regerado, link | CI verde + veredito do revisor | — |
| **Normal** | Documento de processo, código com teste, template sem workflow | CI verde + veredito do revisor | Preview verde |
| **Sensível** | Workflow de CI, permissões, ferramentas de agente, segredos, dependência ou skill nova, regra de governança | CI verde + veredito do revisor + etiqueta "precisa do Samuel" + «Aprovado (aval do Samuel delegado ao Tzu)» na HEAD final | Preview verde + smoke test |
| **Crítica** | Produção de cliente, dado pessoal, pagamento, migração de banco, auth | Tudo da classe sensível (incluindo «Aprovado (aval do Samuel delegado ao Tzu)» na HEAD final) | Smoke test em staging e deploy em produção com A2 |

- Na dúvida entre duas classes, vale a mais alta (mesma regra da governança).
- O aval delegado ao Tzu cobre o merge de PRs e mudanças de permissões, acessos e ferramentas de agente no repositório; não cobre deploy em produção, dinheiro e gasto, comunicação externa/clientes nem dados pessoais, que pertencem ao Samuel (regra definitiva).
- **Trivial sem revisor** (merge só com CI verde) fica **adiado**: só depois que a VTX-214 conferir os checks por script e houver aceite no mesmo modo dos PRs sensíveis (veredito delegado do revisor de IA). Até lá, todo PR tem veredito do revisor. O autor (Sys) não pede aprovação ao Samuel; o revisor de IA pode consultar a opinião dele antes de dar o aval.
- **Smoke test:** o mínimo que prova que o sistema sobe e o caminho principal responde (abrir a página inicial, chamar o endpoint de saúde, fazer login de teste). Fica no runbook do projeto e roda no preview ou no staging, nunca contra dado real de cliente.

## 5. Exemplo

PR que adiciona um job ao `.github/workflows/testes.yml`: classe sensível. O agente roda os testes locais, abre o PR com a etiqueta "precisa do Samuel", espera o CI, corrige um erro de YAML (1ª tentativa), recebe «Aprovado (aval do Samuel delegado ao Tzu)» do revisor de IA na HEAD nova e deixa o PR pronto. O merge acontece com CI verde e esse veredito. O autor (Sys) não pede aprovação ao Samuel; o revisor de IA pode consultar a opinião dele antes de dar o aval.

## 6. Checklist

- [ ] Verificação local feita antes de abrir o PR
- [ ] CI verde na HEAD final, sem teste removido nem limiar baixado
- [ ] Veredito do revisor na HEAD final (depois de ressalvas, veredito novo nessa HEAD)
- [ ] Classe de risco declarada na descrição do PR; etiqueta "precisa do Samuel" quando sensível ou crítica, com veredito «Aprovado (aval do Samuel delegado ao Tzu)» na HEAD final
- [ ] Smoke test em preview ou staging quando a classe pede

## Fontes

- Google, "Code Review Developer Guide": https://google.github.io/eng-practices/review/
- DORA, capacidade "Code maintainability" e lotes pequenos: https://dora.dev/capabilities/
- GitHub Docs, proteção de branch (indisponível em repositório privado no plano Free): https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
