#!/usr/bin/env python3
import sys, yaml
from pathlib import Path

REQUIRED_TOP_LEVEL = ["version", "description", "constraints", "hash_include"]
REQUIRED_CONSTRAINT_KEYS = [
    "budget_cap_usd",
    "allowed_jurisdictions",
    "pii_handling",
    "min_sla_percent",
    "max_latency_ms",
    "data_egress_rules",
    "risk_thresholds",
]
REQUIRED_EGRESS_KEYS = ["non_eu_egress_allowed", "permitted_endpoints"]
REQUIRED_RISK_KEYS = ["max_stockout_risk", "max_delay_minutes"]

def fail(msg):
    print(f"Policy validation failed: {msg}", file=sys.stderr)
    sys.exit(1)

def main():
    path = Path("policies/base.yaml")
    if not path.exists():
        fail("policies/base.yaml not found")

    try:
        doc = yaml.safe_load(path.read_text())
    except Exception as e:
        fail(f"YAML parsing error: {e}")

    if not isinstance(doc, dict):
        fail("Top-level document must be a mapping")

    # Top-level required keys
    missing = [k for k in REQUIRED_TOP_LEVEL if k not in doc]
    if missing:
        fail(f"Missing top-level keys: {missing}")

    # Constraints presence and structure
    constraints = doc.get("constraints")
    if not isinstance(constraints, dict):
        fail("constraints must be a mapping")

    missing_c = [k for k in REQUIRED_CONSTRAINT_KEYS if k not in constraints]
    if missing_c:
        fail(f"Missing constraints keys: {missing_c}")

    # Types and ranges for common fields
    if not isinstance(constraints["budget_cap_usd"], int) or constraints["budget_cap_usd"] < 0:
        fail("constraints.budget_cap_usd must be a non-negative integer")

    if not isinstance(constraints["allowed_jurisdictions"], list) or not all(isinstance(x, str) for x in constraints["allowed_jurisdictions"]):
        fail("constraints.allowed_jurisdictions must be a list of strings")

    if not isinstance(constraints["pii_handling"], str):
        fail("constraints.pii_handling must be a string")

    if not isinstance(constraints["min_sla_percent"], int) or not (0 <= constraints["min_sla_percent"] <= 100):
        fail("constraints.min_sla_percent must be an integer between 0 and 100")

    if not isinstance(constraints["max_latency_ms"], int) or constraints["max_latency_ms"] <= 0:
        fail("constraints.max_latency_ms must be a positive integer")

    # Egress
    egress = constraints["data_egress_rules"]
    if not isinstance(egress, dict):
        fail("constraints.data_egress_rules must be a mapping")
    missing_e = [k for k in REQUIRED_EGRESS_KEYS if k not in egress]
    if missing_e:
        fail(f"Missing data_egress_rules keys: {missing_e}")
    if not isinstance(egress["non_eu_egress_allowed"], bool):
        fail("constraints.data_egress_rules.non_eu_egress_allowed must be a boolean")
    if not isinstance(egress["permitted_endpoints"], list) or not all(isinstance(x, str) for x in egress["permitted_endpoints"]):
        fail("constraints.data_egress_rules.permitted_endpoints must be a list of strings")

    # Risk thresholds
    risk = constraints["risk_thresholds"]
    if not isinstance(risk, dict):
        fail("constraints.risk_thresholds must be a mapping")
    missing_r = [k for k in REQUIRED_RISK_KEYS if k not in risk]
    if missing_r:
        fail(f"Missing risk_thresholds keys: {missing_r}")
    if not isinstance(risk["max_stockout_risk"], (int, float)) or not (0 <= risk["max_stockout_risk"] <= 1):
        fail("constraints.risk_thresholds.max_stockout_risk must be a number between 0 and 1")
    if not isinstance(risk["max_delay_minutes"], int) or risk["max_delay_minutes"] < 0:
        fail("constraints.risk_thresholds.max_delay_minutes must be a non-negative integer")

    # hash_include presence and type
    hi = doc.get("hash_include")
    if not isinstance(hi, list) or not all(isinstance(x, str) for x in hi):
        fail("hash_include must be a list of string paths")

    print("Policy validation OK")

if __name__ == "__main__":
    main()
