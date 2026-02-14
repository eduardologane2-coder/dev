import json
from pathlib import Path
from datetime import datetime

STRATEGY_FILE = Path("/srv/dev/strategy.json")

STAGE_RULES = {
    "basic": lambda m: m["commits"] >= 3,
    "intermediate": lambda m: m["commits"] >= 10 and m["executions"] >= 10,
    "advanced": lambda m: m["selfmods"] >= 3 and m["rollbacks"] >= 1,
    "strategic": lambda m: m["commits"] >= 20 and m["selfmods"] >= 5
}

def evaluate_stage(metrics):
    current = "basic"
    for stage, rule in STAGE_RULES.items():
        if rule(metrics):
            current = stage
    return current

def update_stage(metrics):
    if not STRATEGY_FILE.exists():
        return

    data = json.loads(STRATEGY_FILE.read_text())
    new_stage = evaluate_stage(metrics)

    if data.get("evolution_stage") != new_stage:
        data["evolution_stage"] = new_stage
        data["evolution_last_update"] = str(datetime.now())
        STRATEGY_FILE.write_text(json.dumps(data, indent=2))
