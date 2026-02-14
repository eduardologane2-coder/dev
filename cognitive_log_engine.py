import json
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("/srv/dev/cognitive_log.json")

def log_decision(decision):
    data = []
    if LOG_FILE.exists():
        data = json.loads(LOG_FILE.read_text())

    data.append({
        "timestamp": str(datetime.now()),
        "state": decision.get("state"),
        "confidence": decision.get("confidence")
    })

    LOG_FILE.write_text(json.dumps(data, indent=2))
