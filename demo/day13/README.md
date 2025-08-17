Title: Day 13 mini demo bundle

Contents:

event_file: <name of the event json>

plan_bundle: <name of the plan json>

sim_results: <name of the sim json>

proof_log: day13_proof.jsonl (hash-chained entries)

chain_head: from chain.meta

adt_usage: day13_adt_usage.json (skipped or minimal)

How to replay:

python scripts/seed_disruption.py

python scripts/generate_plans.py

python scripts/verify_policies.py

python scripts/simulate_twin.py

python scripts/write_proof.py

python scripts/adt_touch.py (optional, set RUN_ADT_TOUCH=true and ADT_INSTANCE_URL)