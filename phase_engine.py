import json
from pathlib import Path
from metacognition_engine import get_meta

PHASE_FILE = Path("/srv/dev/phase_state.json")

def _load():
    if not PHASE_FILE.exists():
        return {"phase": "TACTICAL"}
    return json.loads(PHASE_FILE.read_text())

def _save(data):
    PHASE_FILE.write_text(json.dumps(data, indent=2))

def evaluate_phase():
    meta = get_meta()
    current = _load()["phase"]

    new_phase = current

    if meta["plan_ratio"] > 0.6 and meta["avg_confidence"] > 0.75:
        new_phase = "STRATEGIC"

    if meta["samples"] > 30 and meta["plan_ratio"] > 0.7:
        new_phase = "ARCHITECTURAL"

    if meta["samples"] > 60 and meta["avg_confidence"] > 0.85:
        new_phase = "AUTONOMOUS"

    _save({"phase": new_phase})
    return new_phase

def get_phase():
    return _load()["phase"]
