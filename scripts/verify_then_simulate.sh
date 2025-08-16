#!/usr/bin/env bash
set -euo pipefail

PLAN="${1:-}"
SNAPSHOT="${2:-}"

if [ -z "$PLAN" ] || [ -z "$SNAPSHOT" ]; then
  echo "Usage: scripts/verify_then_simulate.sh <plan.json> <twin_snapshot.json>"
  exit 1
fi

# Basic existence checks
if [ ! -f "$PLAN" ]; then
  echo "Error: plan file not found: $PLAN"
  exit 1
fi

if [ ! -f "$SNAPSHOT" ]; then
  echo "Error: snapshot file not found: $SNAPSHOT"
  exit 1
fi

# Verify first
VERDICT_JSON="$(python verifiers/verify_plan.py "$PLAN" 2>&1 || true)"
echo "$VERDICT_JSON"

# Extract "status":"..." (grep/sed only, no heredoc/Python inline)
STATUS="$(printf '%s\n' "$VERDICT_JSON" \
  | tr -d '\n' \
  | sed -n 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"

if [ -z "${STATUS:-}" ]; then
  STATUS="UNKNOWN"
fi

if [ "$STATUS" != "PASS" ]; then
  echo "Verification failed; skipping simulation."
  exit 2
fi

# Simulate if PASS
python verifiers/simulator.py "$SNAPSHOT" "$PLAN"
