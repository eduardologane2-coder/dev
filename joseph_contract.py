import json
from datetime import datetime
from pathlib import Path

JOSEPH_STATE_FILE = Path("/srv/dev/joseph_state.json")

def load_joseph_state():
    if not JOSEPH_STATE_FILE.exists():
        return {"version": 1, "last_update": None, "events": []}
    return json.loads(JOSEPH_STATE_FILE.read_text())

def save_joseph_state(data):
    data["last_update"] = str(datetime.now())
    JOSEPH_STATE_FILE.write_text(json.dumps(data, indent=2))

def register_event(event_type, payload):
    data = load_joseph_state()
    data["events"].append({
        "type": event_type,
        "payload": payload,
        "timestamp": str(datetime.now())
    })
    save_joseph_state(data)
