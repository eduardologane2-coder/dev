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
    return json.loads(METRICS_FILE.read_text())

def _save(data):
    METRICS_FILE.write_text(json.dumps(data, indent=2))

def inc(key: str):
    data = _load()
    if key not in data:
        data[key] = 0
    data[key] += 1
    data["last_update"] = str(datetime.now())
    _save(data)

def metrics_status():
    data = _load()
    return (
        "📊 MÉTRICAS DO DEV\n\n"
        f"Execuções: {data.get('executions',0)}\n"
        f"Commits: {data.get('commits',0)}\n"
        f"SelfMods: {data.get('selfmods',0)}\n"
        f"Falhas: {data.get('failures',0)}\n"
        f"Rollbacks: {data.get('rollbacks',0)}\n"
        f"Última atualização: {data.get('last_update')}"
    )
