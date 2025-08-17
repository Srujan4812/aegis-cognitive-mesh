#!/usr/bin/env python3
import sys, json
from hub.secret_gate import get_secret_if_attested

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
