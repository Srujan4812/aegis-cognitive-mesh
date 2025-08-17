#!/usr/bin/env bash
set -euo pipefail
SECRET_NAME="${1:-acm-demo-ephemeral}"
JWT_FILE="${2:-audits/snp_token.jwt}"

# Use SEV-SNP policy
export ACM_POLICY=sevsnp

# If the JWT doesn’t exist yet, try to fetch it (will fail gracefully off-VM)
if [[ ! -s "$JWT_FILE" ]]; then
  echo "[info] ${JWT_FILE} not found; attempting to fetch from SNP guest..."
  if ./scripts/fetch_snp_jwt.sh "$JWT_FILE"; then
    echo "[ok] fetched SNP JWT"
  else
    echo "[warn] fetch failed or not SNP environment; ensure a real token at $JWT_FILE"
  fi
fi

# Run the gate in SEV-SNP mode
./scripts/run_gate.sh "$SECRET_NAME" "$JWT_FILE"
