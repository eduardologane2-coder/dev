import json
from datetime import datetime
from pathlib import Path

PLAN_FILE = Path("/srv/dev/long_term_plan.json")

def load_plan():
    return json.loads(PLAN_FILE.read_text())

def save_plan(data):
    PLAN_FILE.write_text(json.dumps(data, indent=2))

def review_plan():
    data = load_plan()
    data["last_review"] = str(datetime.now())
    save_plan(data)
    return data["last_review"]

def mark_milestone_completed(milestone_id):
    data = load_plan()
    for m in data["milestones"]:
        if m["id"] == milestone_id:
            m["completed"] = True
    save_plan(data)
