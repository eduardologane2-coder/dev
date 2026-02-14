import json
from datetime import datetime
from pathlib import Path

DEV_DIR = Path("/srv/dev")
PLAN_FILE = DEV_DIR / "long_term_plan.json"
STRATEGY_FILE = DEV_DIR / "strategy.json"

def load_plan():
    return json.loads(PLAN_FILE.read_text())

def save_plan(data):
    PLAN_FILE.write_text(json.dumps(data, indent=2))

def load_strategy():
    return json.loads(STRATEGY_FILE.read_text())

def review_plan():
    plan = load_plan()
    plan["last_review"] = str(datetime.now())
    save_plan(plan)

def sync_with_evolution():
    plan = load_plan()
    strategy = load_strategy()

    stage = strategy.get("evolution_stage")

    for m in plan["milestones"]:
        if m["id"] == "M1" and stage in ["strategic", "architectural", "self_evolving"]:
            m["completed"] = True
        if m["id"] == "M2" and stage in ["architectural", "self_evolving"]:
            m["completed"] = True
        if m["id"] == "M3" and stage == "self_evolving":
            m["completed"] = True

    plan["last_review"] = str(datetime.now())
    save_plan(plan)
