#!/usr/bin/env bash
set -euo pipefail

# Config
SECRET_NAME="${1:-acm-demo-ephemeral}"
JWT_FILE="${2:-audits/day15_token.jwt}"
POLICY_MODE="${ACM_POLICY:-simulated}"  # simulated|sevsnp

mkdir -p audits

# 1) Call the gate and capture two JSON lines (audit + release)
OUT="$(PYTHONPATH=. scripts/attested_get_secret.py "$SECRET_NAME" "$JWT_FILE")" || true
echo "$OUT"

# Parse fields with jq
ATT_TYPE="$(echo "$OUT" | sed -n '1p' | jq -r '.audit.attestation_type // "unknown"')"
RELEASED="$(echo "$OUT" | sed -n '2p' | jq -r '.released // false')"
VALUE="$(echo "$OUT" | sed -n '2p' | jq -r '.value // empty')"

# 2) Fail closed if not released
if [[ "$RELEASED" != "true" ]]; then
  echo "[deny] Runbook blocked: secret not released."
  exit 3
fi

# 3) Minimal approved action (placeholder)
ACTION="approved_action"
ACTION_RESULT="ok"
echo "[ok] Approved action executed."

# 4) Hash-chained audit entry
CHAIN_FILE="audits/chain.log"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
PREV_HASH="$(tail -n 1 "$CHAIN_FILE" 2>/dev/null | jq -r '.hash // empty')"

# Build entry without hash first
ENTRY="$(jq -n \
  --arg ts "$TS" \
  --arg policy "$POLICY_MODE" \
  --arg att "$ATT_TYPE" \
  --arg released "$RELEASED" \
  --arg action "$ACTION" \
  --arg result "$ACTION_RESULT" \
  --arg prev "${PREV_HASH:-}" \
  '{
    ts:$ts,
    policy_mode:$policy,
    attestation_type:$att,
    released:($released=="true"),
    action:$action,
    result:$result,
    prev_hash:($prev|select(.!=""))
  }'
)"

# Compute hash over canonical JSON
HASH="$(printf "%s" "$ENTRY" | jq -c '.' | sha256sum | awk '{print $1}')"
FINAL="$(echo "$ENTRY" | jq --arg h "$HASH" '. + {hash:$h}')"

echo "$FINAL" | tee -a "$CHAIN_FILE" >/dev/null
echo "[ok] Audit appended to $CHAIN_FILE"
