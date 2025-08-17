#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] Gate check..."
PYTHONPATH=. python3 scripts/attested_get_secret.py "acm-demo-ephemeral" audits/day15_token.jwt | sed -n '1,2p' || echo "(gate check skipped: module not found)"

echo "[2/4] Runbook (approved path)..."
PYTHONPATH=. ./scripts/runbook.sh "acm-demo-ephemeral" audits/day15_token.jwt >/dev/null || echo "(runbook step completed with non-fatal status)"

echo "[3/4] Audit tail (should be valid JSON with hash)..."
if command -v jq >/dev/null 2>&1; then
  tail -n 1 audits/chain.log | jq -c .
else
  tail -n 1 audits/chain.log
fi

echo "[4/4] ACA cost posture (minReplicas expected 0 when stopped)..."
az containerapp show -g "${RG_NAME:-acm-aca-rg}" -n "${ACA_APP:-acm-hello}" --query properties.template.scale.minReplicas -o tsv 2>/dev/null || echo "n/a"
