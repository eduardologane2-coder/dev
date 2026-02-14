import json
from datetime import datetime
from pathlib import Path

DEV_DIR = Path("/srv/dev")
METRICS_FILE = DEV_DIR / "metrics.json"

def load_metrics():
    if not METRICS_FILE.exists():
        return {
            "executions": 0,
            "commits": 0,
            "selfmods": 0,
            "failures": 0,
            "rollbacks": 0,
            "last_update": None
        }
    return json.loads(METRICS_FILE.read_text())

def save_metrics(data):
    data["last_update"] = str(datetime.now())
    METRICS_FILE.write_text(json.dumps(data, indent=2))

def increment(field):
    data = load_metrics()
    if field in data:
        data[field] += 1
    save_metrics(data)

def get_metrics():
    return load_metrics()
