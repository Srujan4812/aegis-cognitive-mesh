#!/usr/bin/env python3
import json, sys, time, os, hashlib

OUT_DIR = "artifacts"
os.makedirs(OUT_DIR, exist_ok=True)

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main():
    if len(sys.argv) < 3:
        print("Usage: write_lineage.py <combined_json> <plan_json>")
        sys.exit(1)

    combined_path = sys.argv[1]
    plan_path = sys.argv[2]

    with open(combined_path, "r") as f:
        combined = json.load(f)
    with open(plan_path, "r") as f:
        plan = json.load(f)

    verify = combined.get("verify", {})
    sim = combined.get("simulation", {})

    datasets = {
        "twin_snapshot_path": os.path.abspath(os.environ.get("SNAPSHOT_PATH", "twin_snapshot.json")),
        "plan_path": os.path.abspath(plan_path),
        "policy_base_path": os.path.abspath("policies/base.yaml"),
        "policy_lock_path": os.path.abspath("policies/policy.lock")
    }

    record = {
        "timestamp": now_iso(),
        "plan_id": plan.get("plan_id", "unknown"),
        "policy_sha256": verify.get("policy_sha256"),
        "verify_status": verify.get("status"),
        "violations": verify.get("violations", []),
        "simulation": sim if sim else None,
        "datasets": datasets
    }

    key_src = f"{record['plan_id']}|{record.get('policy_sha256')}|{record['timestamp']}"
    fname = f"lineage_{sha256_text(key_src)[:16]}.json"
    out_path = os.path.join(OUT_DIR, fname)

    with open(out_path, "w") as f:
        json.dump(record, f, indent=2)

    print(out_path)

if __name__ == "__main__":
    main()
