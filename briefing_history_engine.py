import json
from pathlib import Path

HISTORY_FILE = Path("/srv/dev/briefing_history.json")

def load_history():
    if not HISTORY_FILE.exists():
        return []
    return json.loads(HISTORY_FILE.read_text())

def append_entry(topic: str, confidence: int):
    history = load_history()
    history.append({
        "topic": topic,
        "confidence": confidence
    })
    HISTORY_FILE.write_text(json.dumps(history, indent=2))
