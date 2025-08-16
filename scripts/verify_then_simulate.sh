#!/usr/bin/env bash
set -euo pipefail

PLAN="${1:-}"
SNAPSHOT="${2:-}"

if [ -z "$PLAN" ] || [ -z "$SNAPSHOT" ]; then
  echo "Usage: scripts/verify_then_simulate.sh <plan.json> <snapshot.json>"
  exit 1
fi

# Verify first
VERDICT_JSON="$(python verifiers/verify_plan.py "$PLAN")"
echo "$VERDICT_JSON" | jq '.' || true

STATUS="$(echo "$VERDICT_JSON" | jq -r '.status' 2>/dev/null || echo "UNKNOWN")"

if [ "$STATUS" != "PASS" ]; then
  echo "Verification failed; skipping simulation."
  exit 2
fi

# Simulate if PASS
python verifiers/simulator.py "$SNAPSHOT" "$PLAN"
