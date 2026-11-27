#!/usr/bin/env bash
# Portão de merge do vtx-core (VTX-214): só chama gh pr merge com CI verde
# e veredito do revisor na HEAD exata.
set -euo pipefail

uso() {
  echo "uso: $0 <numero-do-pr>" >&2
  exit 2
}

[[ $# -eq 1 && "$1" =~ ^[0-9]+$ ]] || uso
PR="$1"

precisa() {
  echo "mesclar_pr: $*" >&2
  exit 1
}

REPO="$(gh repo view --json nameWithOwner --jq '.nameWithOwner')"
meta="$(gh pr view "$PR" --json headRefOid,state,labels,url)"
estado="$(printf '%s' "$meta" | jq -r '.state')"
sha="$(printf '%s' "$meta" | jq -r '.headRefOid')"
url="$(printf '%s' "$meta" | jq -r '.url')"
sensivel="$(printf '%s' "$meta" | jq -r '[.labels[].name] | index("precisa do Samuel") | if . then "sim" else "nao" end')"

[[ "$estado" == "OPEN" ]] || precisa "PR #$PR não está aberto (estado=$estado)."
[[ "$sha" =~ ^[0-9a-f]{40}$ ]] || precisa "não consegui ler a HEAD do PR #$PR."

curto="${sha:0:7}"

# Campos reais de `gh pr checks --json` (gh 2.103.0): bucket, completedAt,
# description, event, link, name, startedAt, state, workflow. Não existe
# `conclusion`. O próprio `gh` classifica `state` em bucket: pass/skipping = ok,
# pending = pendente, fail/cancel = vermelho. Sem `|| true` o comando sai 1
# (vermelho) ou 8 (pendente) e, com set -e, o script morreria antes de recusar.
checks_json="$(gh pr checks "$PR" --json name,state,bucket || true)"
printf '%s' "$checks_json" | jq -e 'type == "array"' >/dev/null \
  || precisa "falha ao ler os checks do PR #$PR."
total="$(printf '%s' "$checks_json" | jq 'length')"
[[ "$total" -gt 0 ]] || precisa "PR #$PR não tem checks."

falha=0
pend=0
ok=0
while IFS=$'\t' read -r bucket name; do
  b="$(printf '%s' "$bucket" | tr '[:upper:]' '[:lower:]')"
  case "$b" in
    pass|skipping) ok=$((ok + 1)) ;;
    pending) pend=$((pend + 1)) ;;
    fail|cancel) falha=$((falha + 1)) ;;
    *) falha=$((falha + 1)) ;;
  esac
done < <(printf '%s' "$checks_json" | jq -r '.[] | [.bucket, .name] | @tsv')

[[ "$falha" -eq 0 ]] || precisa "PR #$PR tem check vermelho ($falha). Recuso o merge."
[[ "$pend" -eq 0 ]] || precisa "PR #$PR tem check pendente ($pend). Recuso o merge."
[[ "$ok" -gt 0 ]] || precisa "PR #$PR não tem check verde."

# Sem --paginate o gh só devolve os 30 comentários mais antigos; jq -s add
# junta as páginas (cada uma é um array) numa lista só.
comentarios="$(gh api --paginate "repos/${REPO}/issues/${PR}/comments" | jq -s 'add')"

# Formato do revisor daqui em diante (primeira linha):
#   **Veredito: <texto>** (HEAD `<sha>`)
# <sha> é prefixo de 7+ hex da HEAD atual (curto ou completo). Na HEAD de
# merge só passa **Aprovado** (ou o aval delegado em PR sensível).
veredito="$(printf '%s' "$comentarios" | jq -r --arg sha "$sha" '
  [ .[]
    | .body
    | capture("(?s)\\*\\*Veredito:\\s*(?<v>[^*\\n]+)\\*\\*[^\\n]*HEAD[ `]*`(?<h>[0-9a-f]{7,40})`")
    | select(.h as $h | $sha | startswith($h))
    | .v
    | gsub("^\\s+|\\s+$";"")
  ] | last // empty
')"

[[ -n "$veredito" ]] || precisa "PR #$PR ($curto) não tem veredito do revisor nesta HEAD no formato «**Veredito: …** (HEAD \`sha\`)». Recuso o merge."

if [[ "$veredito" == "Aprovado com ressalvas"* ]]; then
  precisa "PR #$PR tem «Aprovado com ressalvas» nesta HEAD; as ressalvas precisam ser aplicadas e pede-se veredito novo (Aprovado) na HEAD final."
fi

if [[ "$sensivel" == "sim" ]]; then
  [[ "$veredito" == "Aprovado (aval do Samuel delegado ao Tzu)" ]] \
    || precisa "PR #$PR é sensível e o veredito nesta HEAD não é «Aprovado (aval do Samuel delegado ao Tzu)» (obtido: $veredito)."
else
  [[ "$veredito" == "Aprovado" ]] \
    || precisa "PR #$PR não está Aprovado nesta HEAD (obtido: $veredito)."
fi

echo "mesclar_pr: #$PR $url HEAD $curto checks ok, veredito: $veredito"
exec gh pr merge "$PR" --squash --match-head-commit "$sha"
