#!/usr/bin/env python3
import sys, json, base64, pathlib, time

def b64url_to_text(seg: str) -> str:
    if isinstance(seg, bytes):
        seg = seg.decode("ascii", errors="ignore")
    seg = seg.strip()
    pad = "=" * (-len(seg) % 4)
    data = base64.urlsafe_b64decode((seg + pad).encode("ascii", errors="ignore"))
    return data.decode("ascii", errors="ignore")

def peek_claims(jwt_text: str):
    parts = jwt_text.strip().split(".")
    if len(parts) != 3 or not parts[1]:
        raise ValueError("Invalid JWT format")
    hdr = json.loads(b64url_to_text(parts[0]))
    pl = json.loads(b64url_to_text(parts[1]))
    return hdr, pl

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <jwt-file>")
        sys.exit(1)

    path = pathlib.Path(sys.argv[1])
    txt = path.read_text(encoding="utf-8", errors="ignore").strip()
    hdr, pl = peek_claims(txt)
    iss = pl.get("iss", "unknown")
    att = pl.get("x-ms-attestation-type", "unknown")
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    out = {
        "timestamp": ts,
        "file": str(path),
        "iss": iss,
        "x-ms-attestation-type": att
    }
    print(json.dumps(out))
    # Append to audits/day17_check.log
    log_path = pathlib.Path("audits/day17_check.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(out) + "\n")

if __name__ == "__main__":
    main()
