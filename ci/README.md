# Workflows pendentes de ativação

`sincronizar-painel.yml` precisa ficar em `.github/workflows/` para rodar. Ele foi salvo aqui porque o token
usado na criação do repositório não tem o escopo `workflow` (o GitHub bloqueia a criação de workflows sem ele).

## Passos para ativar (Samuel)

1. **Criar o token do painel** — GitHub → Settings → Developer settings → Personal access tokens → *Fine-grained tokens* → *Generate new token*:
   - Repository access: *Only select repositories* → `vtx_painel`
   - Permissions → Repository → **Contents: Read and write** (Metadata: Read fica automático)
   - Validade: à sua escolha (ex.: 1 ano)
2. **Salvar como segredo** em `vtx-core` → Settings → Secrets and variables → Actions → *New repository secret*:
   - Nome: `PANEL_TOKEN` · Valor: o token do passo 1
3. **Ativar o workflow**: no GitHub web, criar o arquivo `.github/workflows/sincronizar-painel.yml` em `vtx-core`
   com o conteúdo de `ci/sincronizar-painel.yml` (ou conceder o escopo `workflow` ao token do agente para que ele mova o arquivo).
4. Rodar manualmente uma vez: Actions → *sincronizar-painel* → *Run workflow*.
