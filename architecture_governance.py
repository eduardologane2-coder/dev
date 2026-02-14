import json
from pathlib import Path
from datetime import datetime

STRATEGY_FILE = Path("/srv/dev/strategy.json")

def register_architecture_event(event_type, description):
    if not STRATEGY_FILE.exists():
        return

    data = json.loads(STRATEGY_FILE.read_text())
    history = data.get("change_history", [])

    history.append({
        "type": event_type,
        "description": description,
        "timestamp": str(datetime.now())
    })

    data["change_history"] = history
    STRATEGY_FILE.write_text(json.dumps(data, indent=2))
