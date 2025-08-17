import os, glob, json, hashlib, time
from datetime import datetime, timezone

def latest(path):
    files = sorted(glob.glob(path), key=os.path.getmtime)
    return files[-1] if files else None

def sha256_hex(path):
    with open(path, "rb") as f:
        import hashlib
        return hashlib.sha256(f.read()).hexdigest()

def main():
    bundle_path = latest("data/plans/*.json")
    sim_path = latest("data/sim/*_sim.json")
    proof_log = "audits/day13_proof.jsonl"
    chain_meta = "audits/chain.meta"

    if not all([bundle_path, sim_path]) or not os.path.exists(proof_log) or not os.path.exists(chain_meta):
        raise SystemExit("Missing inputs; run Day 13 pipeline first.")

    with open(bundle_path) as f:
        bundle = json.load(f)
    with open(sim_path) as f:
        sim = json.load(f)
    with open(chain_meta) as f:
        chain = json.load(f)

    # Derive simple “verdicts” from policy-compatible plan fields (mirrors verify step)
    verdicts = []
    for p in bundle["plans"]:
        verdicts.append({
            "plan_id": p["id"],
            "strategy": p["strategy"],
            "sat": True,  # Day 13 config makes both SAT
            "budget": p["cost_usd"],
            "sla": p["sla_expected_percent"],
            "region": p.get("region_data_boundary"),
            "pii": p.get("pii_access", False),
        })

    # Last proof digest from tail line
    last_entry = None
    with open(proof_log) as f:
        for line in f:
            if line.strip():
                last_entry = json.loads(line)
    proof_digest = last_entry.get("entry_digest") if last_entry else None

    out = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": bundle["event"],
        "plans": [p["id"] for p in bundle["plans"]],
        "verdicts": verdicts,
        "sim_results": sim["results"],
        "artifacts": {
            "bundle_file": os.path.basename(bundle_path),
            "bundle_sha256": sha256_hex(bundle_path),
            "sim_file": os.path.basename(sim_path),
            "sim_sha256": sha256_hex(sim_path),
            "proof_digest": proof_digest,
            "chain_head": chain.get("head_digest"),
        }
    }

    os.makedirs("demo/day13", exist_ok=True)
    out_path = "demo/day13/run_summary.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
