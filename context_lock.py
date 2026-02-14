from pathlib import Path
import json

LOCK_FILE = Path("/srv/dev/context_lock.json")

def load_lock():
    if not LOCK_FILE.exists():
        return {"briefing_active": False}
    return json.loads(LOCK_FILE.read_text())

def save_lock(state):
    LOCK_FILE.write_text(json.dumps(state, indent=2))

def activate_briefing():
    save_lock({"briefing_active": True})

def deactivate_briefing():
    save_lock({"briefing_active": False})

def is_briefing_active():
    return load_lock().get("briefing_active", False)
