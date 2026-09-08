#!/usr/bin/env bash
# deploy-mcp.sh — CasePal Lab 5: deploy the mock case-management MCP server.
# Usage: ./deploy-mcp.sh (override with env: RESOURCE_GROUP, APP_NAME, ENVIRONMENT, LOCATION)
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-casepal-mcp}"
APP_NAME="${APP_NAME:-casepal-case-management}"
ENVIRONMENT="${ENVIRONMENT:-casepal-mcp-env}"
LOCATION="${LOCATION:-swedencentral}"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "Deploying $APP_NAME to $RESOURCE_GROUP ($LOCATION)..."
az group create -n "$RESOURCE_GROUP" -l "$LOCATION" -o none

az containerapp up \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$ENVIRONMENT" \
  --location "$LOCATION" \
  --source "$HERE" \
  --ingress external \
  --target-port 8000 \
  --env-vars PORT=8000

FQDN=$(az containerapp show -n "$APP_NAME" -g "$RESOURCE_GROUP" --query "properties.configuration.ingress.fqdn" -o tsv)
echo ""
echo "MCP endpoint (share with participants):"
echo "  https://$FQDN/mcp"
echo "Auth: None. Approval: require approval for create_case and update_case_status in Foundry."
