<#
  deploy-mcp.ps1 — CasePal Lab 5: deploy the mock case-management MCP server.

  Pushes mcp-case-management/ to Azure Container Apps with public, no-auth ingress, then prints
  the /mcp URL to paste into the Foundry agent's MCP tool. Synthetic data only.
#>
param(
  [string]$ResourceGroup = "rg-casepal-mcp",
  [string]$AppName       = "casepal-case-management",
  [string]$Environment   = "casepal-mcp-env",
  [string]$Location      = "swedencentral"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Deploying $AppName to $ResourceGroup ($Location)..." -ForegroundColor Cyan
az group create -n $ResourceGroup -l $Location -o none

az containerapp up `
  --name $AppName `
  --resource-group $ResourceGroup `
  --environment $Environment `
  --location $Location `
  --source $here `
  --ingress external `
  --target-port 8000 `
  --env-vars PORT=8000

$fqdn = az containerapp show -n $AppName -g $ResourceGroup --query "properties.configuration.ingress.fqdn" -o tsv
$url  = "https://$fqdn/mcp"
Write-Host ""
Write-Host "MCP endpoint (share with participants):" -ForegroundColor Green
Write-Host "  $url" -ForegroundColor Yellow
Write-Host "Auth: None. Approval: require approval for create_case and update_case_status in Foundry."
