#!/usr/bin/env bash
# Assign Foundry RBAC for the CasePal workshop (20 participants + 1 facilitator).
#   Foundry User            -> each attendee   (build + run agents; data plane)
#   Foundry Project Manager -> facilitator     (can Publish the Lab 5B hosted agent)
# Uses role IDs (not names) — the Foundry roles were recently renamed
# (Azure AI User -> Foundry User). Docs: https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry
#
# Prereq: `az login` as Owner / User Access Administrator on the resource. Get the id with:
#   az cognitiveservices account show -n <foundry-account> -g <rg> --query id -o tsv
#
# Usage: ./assign-foundry-rbac.sh <foundry-resource-id> [attendees-file] [facilitator-upn]
set -euo pipefail

RESOURCE_ID="${1:?Pass the Foundry resource id (az cognitiveservices account show ... --query id -o tsv)}"
ATTENDEES="${2:-attendees.txt}"
FACILITATOR="${3:-}"

FOUNDRY_USER="53ca6127-db72-4b80-b1b0-d745d6d5456d"
FOUNDRY_PROJECT_MANAGER="eadc314b-1a2d-4efa-be10-5d325db5065e"

[ -f "$ATTENDEES" ] || { echo "Attendees file not found: $ATTENDEES (copy attendees.example.txt)"; exit 1; }

echo "Assigning Foundry User on $RESOURCE_ID"
grep -vE '^\s*(#|$)' "$ATTENDEES" | while IFS= read -r upn; do
  upn="$(echo "$upn" | xargs)"   # trim
  [ -z "$upn" ] && continue
  echo "  + Foundry User -> $upn"
  az role assignment create --role "$FOUNDRY_USER" --assignee "$upn" --scope "$RESOURCE_ID" --only-show-errors >/dev/null
done

if [ -n "$FACILITATOR" ]; then
  echo "  + Foundry Project Manager -> $FACILITATOR (Lab 5B publish demo)"
  az role assignment create --role "$FOUNDRY_PROJECT_MANAGER" --assignee "$FACILITATOR" --scope "$RESOURCE_ID" --only-show-errors >/dev/null
fi

echo "Done. Verify: az role assignment list --assignee <upn> --scope $RESOURCE_ID -o table"
