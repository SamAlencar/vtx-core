# Regras do Cursor (padrão VTX)

Base criada pelo Samuel em 20/10/2026. Todo repositório de projeto da VTX recebe na raiz:
- `.cursorignore` → raiz do repo.
- `eficiencia-de-tokens.mdc` → `.cursor/rules/` (formato atual do Cursor; o `.cursorrules` na raiz é legado, mas o conteúdo é o mesmo).

Adaptações feitas pelo Sys (conservadoras): modo autônomo para as regras que pedem "pergunte/aguarde Ok"; `*.svg` liberado em projetos web; `.next/` incluído; exceção `!arquivo` para CSV/PDF que sejam insumo. Já aplicado no próprio vtx-core.
