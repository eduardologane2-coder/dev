from pathlib import Path
import json

STATE_FILE = Path("/srv/dev/.selfmod/architecture_state.json")

def load_state():
    if not STATE_FILE.exists():
        return {"version": 1, "stability_score": 1.0}
    return json.loads(STATE_FILE.read_text())

def save_state(state):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def evolve(score_delta):
    state = load_state()
    state["stability_score"] = max(0.0, state["stability_score"] + score_delta)
    save_state(state)
