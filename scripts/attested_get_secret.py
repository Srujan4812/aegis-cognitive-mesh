#!/usr/bin/env python3
import sys
import json
import base64

from hub.secret_gate import get_secret_if_attested

def _peek_attestation_type(compact: str) -> str:
    """
    Lightweight, best-effort extractor for x-ms-attestation-type from the JWT payload.
    - Does not verify signature.
    - Tolerates empty signature.
    - Returns "unknown" on any parsing issue.
    """
    try:
        parts = compact.strip().split(".")
        if len(parts) != 3 or not parts[1]:
            return "unknown"
        seg = parts[1]  # ✅ payload segment only
        # Base64URL padding
        pad = "=" * (-len(seg) % 4)
        payload_b = base64.urlsafe_b64decode((seg + pad).encode("ascii", errors="ignore"))
        payload_txt = payload_b.decode("ascii", errors="ignore")
        data = json.loads(payload_txt)
        return data.get("x-ms-attestation-type", "unknown")
    except Exception:
        return "unknown"

def main():
    if len(sys.argv) < 3:
        print("Usage: attested_get_secret.py <secret_name> <jwt_file>")
        sys.exit(1)

    secret_name, jwt_file = sys.argv[1], sys.argv[2]

    try:
        with open(jwt_file, "r", encoding="utf-8") as f:
            maa_jwt = f.read().strip()
    except Exception as e:
        print(json.dumps({"secret_name": secret_name, "released": False, "error": f"Read error: {e}"}))
        sys.exit(2)

    # Day 16: print audit line for attestation type (simulated vs sevsnpvm)
    att_type = _peek_attestation_type(maa_jwt)
    print(json.dumps({"audit": {"attestation_type": att_type}}))

    try:
        val = get_secret_if_attested(secret_name, maa_jwt)
        print(json.dumps({
            "secret_name": secret_name,
            "released": val is not None,
            "value": val if val is not None else None
        }))
        sys.exit(0 if val is not None else 3)
    except Exception as e:
        print(json.dumps({"secret_name": secret_name, "released": False, "error": f"Secret gate error: {e}"}))
        sys.exit(4)

if __name__ == "__main__":
    main()
