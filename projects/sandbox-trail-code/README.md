# Sandbox Trail-code (VTX-135)

Piloto local do [trailhq/Trail-Code](https://github.com/trailhq/Trail-Code/tree/b1211ef) (MIT, pin `b1211ef`). Não é um produto VTX.

**Decisão: adotado com restrições.** O mapa local (`graft build` / `ask` / `skeleton` / `check`, sem `--deep`) pode ser usado como ferramenta do [mapa de codebase](../../knowledge/engenharia/mapa-de-codebase.md). Ficam de fora: `init`, `build --deep`, Trail workspace, MCP no vtx-core, instalação na raiz ou com `-g`, e `graft upgrade` para fora do pin. Relato em [piloto-trail-code.md](../../knowledge/ferramentas/piloto-trail-code.md).

No pin o pacote npm é `@nanonets/graft@0.23.1` e o binário é `graft` (não `trail`). Telemetria desligada com `DO_NOT_TRACK=1` antes do `npm ci` e `graft telemetry disable`. `HOME` e o cache npm ficam dentro deste diretório (gitignorados).

Para repetir o piloto: `scripts/rodar-piloto.sh` (usa `npm ci --ignore-scripts` e o `package-lock.json` versionado). A saída nova vai para `exemplos/saida-bruta/` (gitignorada) e não sobrescreve as amostras versionadas em `exemplos/`. Não versione `node_modules/`, `.home/`, `.npm-cache/`, `.trail/` nem `tmp-repo/`.
