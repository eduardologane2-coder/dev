import json
from pathlib import Path
from datetime import datetime

FILE = Path("/srv/dev/cognitive_metrics.json")

def _base():
    return {
        "total": 0,
        "EXECUTE": 0,
        "PLAN": 0,
        "REJECT": 0,
        "CONFIRM": 0,
        "BRIEFING": 0,
        "avg_confidence": 0.0,
        "last_update": None
    }

def load():
    if not FILE.exists():
        return _base()
    return json.loads(FILE.read_text())

def save(data):
    FILE.write_text(json.dumps(data, indent=2))

def register_decision(decision_data: dict):
    data = load()

    state = decision_data["state"]
    confidence = decision_data["confidence"]

    data["total"] += 1
    if state in data:
        data[state] += 1

    # média incremental simples
    data["avg_confidence"] = (
        (data["avg_confidence"] * (data["total"] - 1) + confidence)
        / data["total"]
    )

    data["last_update"] = str(datetime.now())

    save(data)
