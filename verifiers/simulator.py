# verifiers/simulator.py
import json, sys

def simulate(snapshot, plan):
    """
    Minimal Day 10 scaffold.
    Input:
      - snapshot: dict representing a tiny twin snapshot
      - plan: dict representing a candidate plan
    Output: dict with KPI deltas (will implement in next step)
    """
    return {
        "plan_id": plan.get("plan_id", "unknown"),
        "cost_delta": plan.get("cost_usd", 0),
        "risk_delta": 0.0,    # TODO: compute in Step 2
        "delay_delta": 0.0,   # TODO: compute in Step 2
        "baseline": {},
        "after": {}
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python verifiers/simulator.py twin_snapshot.json plan.json")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        snapshot = json.load(f)
    with open(sys.argv, "r") as f:
        plan = json.load(f)

    result = simulate(snapshot, plan)
    print(json.dumps(result, indent=2))
