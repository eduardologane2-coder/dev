import json
from pathlib import Path
from datetime import datetime

SEMANTIC_FILE = Path("/srv/dev/semantic_memory.json")

def _load():
    if not SEMANTIC_FILE.exists():
        return {"patterns": [], "last_update": None}
    return json.loads(SEMANTIC_FILE.read_text())

def _save(data):
    SEMANTIC_FILE.write_text(json.dumps(data, indent=2))

def register_pattern(topic: str, decision_state: str, confidence: float):
    data = _load()

    entry = {
        "timestamp": str(datetime.now()),
        "topic": topic,
        "state": decision_state,
        "confidence": confidence
    }

    data["patterns"].append(entry)
    data["last_update"] = str(datetime.now())

    _save(data)

def get_recent_patterns(limit=5):
    data = _load()
    return data["patterns"][-limit:]
