#!/usr/bin/env bash
set -euo pipefail
SECRET_NAME="${1:-acm-demo-ephemeral}"
JWT_FILE="${2:-audits/day15_token.jwt}"
POLICY="${ACM_POLICY:-simulated}"  # simulated | sevsnp

if [[ "$POLICY" == "sevsnp" ]]; then
  export ACM_POLICY_FILE="policies/skr.release.sevsnp.json"
else
  export ACM_POLICY_FILE="policies/skr.release.json"
fi

PYTHONPATH=. scripts/attested_get_secret.py "$SECRET_NAME" "$JWT_FILE"
