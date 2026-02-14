import json
from pathlib import Path
from datetime import datetime

METRICS_FILE = Path("/srv/dev/metrics.json")

DEFAULT_METRICS = {
    "executions": 0,
    "commits": 0,
    "selfmods": 0,
    "failures": 0,
    "rollbacks": 0,
    "last_update": None
}

def _load():
    if not METRICS_FILE.exists():
        METRICS_FILE.write_text(json.dumps(DEFAULT_METRICS, indent=2))
        return DEFAULT_METRICS.copy()
    return json.loads(METRICS_FILE.read_text())

def _save(data):
    data["last_update"] = str(datetime.now())
    METRICS_FILE.write_text(json.dumps(data, indent=2))

def inc(key):
    data = _load()
    if key in data:
        data[key] += 1
    _save(data)

def get_metrics():
    return _load()
