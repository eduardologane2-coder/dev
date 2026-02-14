import json
from pathlib import Path

STATE_FILE = Path("/srv/dev/context_lock.json")

def load():
    if not STATE_FILE.exists():
        return {"score": 0}
    return json.loads(STATE_FILE.read_text())

def save(data):
    STATE_FILE.write_text(json.dumps(data, indent=2))

def increase(weight=1):
    state = load()
    state["score"] = state.get("score", 0) + weight
    save(state)

def decrease(weight=1):
    state = load()
    state["score"] = max(0, state.get("score", 0) - weight)
    save(state)

def get_score():
    return load().get("score", 0)
