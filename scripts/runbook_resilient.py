#!/usr/bin/env python3
import json
import os
import sys
import subprocess
import hashlib, time, pathlib  # <-- added
from scripts.lib_retry import retry


def call_gate(secret_name: str, token_path: str):
    """
    Ask the gate if the secret can be released.
    Returns (ok, msg). ok=True only if the final JSON line has released:true.
    """
    try:
        # Call the gate script with a clean argv list and explicit env
        cmd = ["python3", "scripts/attested_get_secret.py", secret_name, token_path]
        env = os.environ.copy()
        env["PYTHONPATH"] = env.get("PYTHONPATH") or "."
        p = subprocess.run(cmd, capture_output=True, text=True, env=env)
        out = p.stdout.strip()

        if p.returncode != 0:
            return False, f"gate_error:{(p.stderr or out).strip()}"

        lines = [l for l in out.splitlines() if l.strip()]
        if not lines:
            return False, "gate_empty_output"

        try:
            release = json.loads(lines[-1])
        except Exception as e:
            return False, f"gate_parse_error:{e}"

        if release.get("released") is True:
            return True, "released:true"
        return False, "released:false"
    except Exception as e:
        return False, f"gate_exception:{e}"


def main():
    if len(sys.argv) < 3:
        print("Usage: runbook_resilient.py <secret_name> <token_path>", file=sys.stderr)
        sys.exit(1)

    secret_name = sys.argv[1]
    token_path = sys.argv[2]

    ok, msg = retry(lambda: call_gate(secret_name, token_path),
                    attempts=5, base_delay=0.3, max_delay=2.0, jitter=0.3)
    if not ok:
        print(f"[deny] Runbook blocked after retries: {msg}")
        sys.exit(2)

    # === Audit logging patch ===
    try:
        token_txt = pathlib.Path(token_path).read_text(encoding="utf-8").strip()
        token_dig = hashlib.sha256(token_txt.encode("utf-8")).hexdigest()[:12]
    except Exception:
        token_dig = None

    audit_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "audit": {"attestation_type": "simulated"},  # later we can propagate real type
        "released": True,
        "secret_name": secret_name,
        "token_digest": token_dig,
    }

    ap = pathlib.Path("audits/chain.log")
    ap.parent.mkdir(parents=True, exist_ok=True)
    with ap.open("a", encoding="utf-8") as f:
        f.write(json.dumps(audit_entry) + "\n")
    # === End audit logging patch ===

    # If released:true, delegate to the existing runbook to perform the approved action
    p = subprocess.run(["bash", "scripts/runbook.sh", secret_name, token_path], text=True)
    sys.exit(p.returncode)


if __name__ == "__main__":
    main()
