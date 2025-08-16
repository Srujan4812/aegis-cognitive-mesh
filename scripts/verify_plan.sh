#!/usr/bin/env bash
set -euo pipefail
PLAN="${1:-}"
if [ -z "$PLAN" ]; then
  echo "Usage: scripts/verify_plan.sh <plan>"
  exit 1
fi
python verifiers/verify_plan.py "$PLAN"
