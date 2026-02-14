import json
from evolution_transition_engine import update_stage

METRICS_FILE = "/srv/dev/metrics.json"

def load_metrics():
    try:
        return json.load(open(METRICS_FILE))
    except:
        return {}

def update_evolution():
    metrics = load_metrics()
    update_stage(metrics)
