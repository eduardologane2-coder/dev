import json
from pathlib import Path

FILE = Path("/srv/dev/briefing_state.json")

def load_state():
    if not FILE.exists():
        return {"active": False, "history": []}
    return json.loads(FILE.read_text())

def save_state(state):
    FILE.write_text(json.dumps(state, indent=2))

def start_briefing(text):
    state = {
        "active": True,
        "history": [{"role": "user", "content": text}]
    }
    save_state(state)

def append_input(text):
    state = load_state()
    state["history"].append({"role": "user", "content": text})
    save_state(state)

def close_briefing():
    save_state({"active": False, "history": []})
