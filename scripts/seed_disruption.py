import json, os, time, hashlib
from datetime import datetime

CONFIG = "configs/day13.yaml"
EVENTS_DIR = "data/events"
os.makedirs(EVENTS_DIR, exist_ok=True)

event = {
    "type": "route_outage",
    "route_id": "R7",
    "warehouse_id": "W3",
    "source": "day13-seed",
    "severity": "high",
    "ts": datetime.utcnow().isoformat() + "Z"
}

payload = json.dumps(event, sort_keys=True).encode()
event_id = hashlib.sha256(payload).hexdigest()[:16]
path = os.path.join(EVENTS_DIR, f"{event_id}.json")

with open(path, "w") as f:
    json.dump(event, f, indent=2)

print(f"Wrote disruption event: {path}")
