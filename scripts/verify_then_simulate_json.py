#!/usr/bin/env python3
import json, sys, subprocess

def run(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    rc = p.returncode
    return rc, out.strip() or "", err.strip() or ""

def main():
    if len(sys.argv) != 3:
        print("Usage: scripts/verify_then_simulate_json.py <plan.json> <twin_snapshot.json>")
        sys.exit(1)

    plan, snapshot = sys.argv[1], sys.argv[2]

    # 1) Verify
    rc, vout, verr = run(["python", "verifiers/verify_plan.py", plan])
    try:
        verify = json.loads(vout)
    except Exception:
        verify = {"status":"UNKNOWN","raw":vout,"stderr":verr}

    # If FAIL, output just the verify JSON
    if verify.get("status") != "PASS":
        print(json.dumps({"verify": verify}, indent=2))
        sys.exit(0)

    # 2) Simulate
    rc, sout, serr = run(["python", "verifiers/simulator.py", snapshot, plan])
    try:
        sim = json.loads(sout)
    except Exception:
        sim = {"error":"simulation_json_parse_error","raw":sout,"stderr":serr}

    # 3) Combined artifact
    combined = {
        "verify": verify,
        "simulation": sim
    }
    print(json.dumps(combined, indent=2))

if __name__ == "__main__":
    main()
