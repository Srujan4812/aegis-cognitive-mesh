#!/usr/bin/env bash
set -euo pipefail
SNAPSHOT="${1:-}"
PLAN="${2:-}"
if [ -z "$SNAPSHOT" ] || [ -z "$PLAN" ]; then
  echo "Usage: scripts/simulate_plan.sh <snapshot.json> <plan.json>"
  exit 1
fi
python verifiers/simulator.py "$SNAPSHOT" "$PLAN"
