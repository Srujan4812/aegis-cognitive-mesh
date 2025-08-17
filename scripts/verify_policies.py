import json, sys, glob, os
from z3 import Real, Bool, Solver, Not, sat

PLANS_DIR = "data/plans"
CONFIG_PATH = "configs/day13.yaml"

def load_latest_bundle():
    files = sorted(glob.glob(os.path.join(PLANS_DIR, "*.json")), key=os.path.getmtime)
    if not files:
        print("No plan bundles found. Run generate_plans.py first.")
        sys.exit(1)
    with open(files[-1]) as f:
        return json.load(f), files[-1]

def load_config():
    import yaml
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def verify_plan(plan, cfg):
    s = Solver()
    cost = Real("cost")
    sla = Real("sla")
    pii = Bool("pii")
    region_ok = Bool("region_ok")

    s.add(cost == float(plan["cost_usd"]))
    s.add(sla == float(plan["sla_expected_percent"]))
    s.add(pii == bool(plan.get("pii_access", False)))
    s.add(region_ok == (plan.get("region_data_boundary") == cfg["region_data_boundary"]))

    budget_cap = float(cfg["budget_cap_usd"])
    sla_min = float(cfg["sla_min_percent"])

    # Policies
    s.add(cost <= budget_cap)    # cost under cap
    s.add(sla >= sla_min)        # SLA above threshold
    s.add(region_ok)             # must match configured boundary
    s.add(Not(pii))              # PII must not be accessed

    verdict = s.check()
    counterexample = None
    if verdict != sat:
        counterexample = str(s.model())
    return verdict == sat, counterexample

def main():
    cfg = load_config()
    bundle, path = load_latest_bundle()
    results = []
    for plan in bundle["plans"]:
        ok, cx = verify_plan(plan, cfg)
        results.append({
            "plan_id": plan["id"],
            "strategy": plan["strategy"],
            "sat": ok,
            "counterexample": cx
        })
    out = {
        "bundle_file": os.path.basename(path),
        "policy_version": cfg["policy_version"],
        "results": results
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
