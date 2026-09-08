<#
.SYNOPSIS
  Assign Foundry RBAC for the CasePal workshop (20 participants + 1 facilitator).

.DESCRIPTION
  - Foundry User  -> each attendee  (build + run agents; data plane)
  - Foundry Project Manager -> facilitator (can Publish the Lab 5B hosted agent)
  Uses role IDs (not names) because the Foundry roles were recently renamed
  (Azure AI User -> Foundry User). Validated against:
  https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry

.PREREQUISITES
  Run `az login` first as someone with Owner or User Access Administrator on the
  Foundry resource. Get the resource id with:
    az cognitiveservices account show -n <foundry-account> -g <rg> --query id -o tsv

.EXAMPLE
  ./assign-foundry-rbac.ps1 -ResourceId "/subscriptions/.../accounts/myfoundry" `
      -AttendeesFile attendees.txt -Facilitator facilitator@contoso.com
#>
param(
  [Parameter(Mandatory = $true)] [string] $ResourceId,
  [string] $AttendeesFile = "attendees.txt",
  [string] $Facilitator
)

$ErrorActionPreference = "Stop"

$FoundryUser           = "53ca6127-db72-4b80-b1b0-d745d6d5456d"
$FoundryProjectManager = "eadc314b-1a2d-4efa-be10-5d325db5065e"

if (-not (Test-Path $AttendeesFile)) {
  throw "Attendees file not found: $AttendeesFile (copy attendees.example.txt and edit it)."
}

$attendees = Get-Content $AttendeesFile |
  Where-Object { $_.Trim() -and -not $_.Trim().StartsWith('#') } |
  ForEach-Object { $_.Trim() }

Write-Host "Assigning Foundry User to $($attendees.Count) attendee(s) on $ResourceId" -ForegroundColor Cyan
foreach ($upn in $attendees) {
  Write-Host "  + Foundry User -> $upn"
  az role assignment create --role $FoundryUser --assignee $upn --scope $ResourceId --only-show-errors | Out-Null
}

if ($Facilitator) {
  Write-Host "Assigning Foundry Project Manager -> $Facilitator (Lab 5B publish demo)" -ForegroundColor Cyan
  az role assignment create --role $FoundryProjectManager --assignee $Facilitator --scope $ResourceId --only-show-errors | Out-Null
}

Write-Host "Done. Verify with: az role assignment list --assignee <upn> --scope $ResourceId -o table" -ForegroundColor Green
