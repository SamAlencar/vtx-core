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

checks_json="$(gh pr checks "$PR" --json name,state,conclusion)"
total="$(printf '%s' "$checks_json" | jq 'length')"
[[ "$total" -gt 0 ]] || precisa "PR #$PR não tem checks."

falha=0
pend=0
ok=0
while IFS=$'\t' read -r state conclusion name; do
  s="$(printf '%s' "$state" | tr '[:lower:]' '[:upper:]')"
  c="$(printf '%s' "$conclusion" | tr '[:lower:]' '[:upper:]')"
  if [[ "$s" == "PENDING" || "$s" == "QUEUED" || "$s" == "IN_PROGRESS" || "$s" == "EXPECTED" || "$c" == "PENDING" ]]; then
    pend=$((pend + 1))
  elif [[ "$c" == "SUCCESS" || "$c" == "SKIPPED" || "$c" == "NEUTRAL" || ( "$s" == "SUCCESS" && -z "$c" ) ]]; then
    ok=$((ok + 1))
  else
    falha=$((falha + 1))
  fi
done < <(printf '%s' "$checks_json" | jq -r '.[] | [.state, (.conclusion // ""), .name] | @tsv')

[[ "$falha" -eq 0 ]] || precisa "PR #$PR tem check vermelho ($falha). Recuso o merge."
[[ "$pend" -eq 0 ]] || precisa "PR #$PR tem check pendente ($pend). Recuso o merge."
[[ "$ok" -gt 0 ]] || precisa "PR #$PR não tem check verde."

comentarios="$(gh api "repos/${REPO}/issues/${PR}/comments")"
veredito="$(printf '%s' "$comentarios" | jq -r --arg sha "$sha" --arg curto "$curto" '
  [ .[]
    | select(.body | test("HEAD[ `]*" + $curto; "i"))
    | .body
    | capture("(?s)\\*\\*Veredito:\\s*(?<v>[^*\\n]+)\\*\\*")
    | .v
    | gsub("^\\s+|\\s+$";"")
  ] | last // empty
')"

[[ -n "$veredito" ]] || precisa "PR #$PR ($curto) não tem veredito do revisor nesta HEAD. Recuso o merge."

if [[ "$sensivel" == "sim" ]]; then
  printf '%s' "$veredito" | grep -Fq "Aprovado (aval do Samuel delegado ao Tzu)" \
    || precisa "PR #$PR é sensível e o veredito nesta HEAD não é «Aprovado (aval do Samuel delegado ao Tzu)» (obtido: $veredito)."
else
  printf '%s' "$veredito" | grep -Eq '^Aprovado( com ressalvas)?($| )' \
    || precisa "PR #$PR não está Aprovado nesta HEAD (obtido: $veredito)."
fi

echo "mesclar_pr: #$PR $url HEAD $curto checks ok, veredito: $veredito"
exec gh pr merge "$PR" --squash --match-head-commit "$sha"
