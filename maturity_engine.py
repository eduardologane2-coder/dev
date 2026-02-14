import json
from pathlib import Path

LOG_FILE = Path("/srv/dev/cognitive_log.json")

RISK_WEIGHTS = {
    "BRIEFING": 0,
    "PLAN_READY": 1,
    "EXECUTE_LOW": 2,
    "EXECUTE_HIGH": 4
}

def classify_risk(entry):
    state = entry.get("state")

    if state == "PLAN_READY":
        return RISK_WEIGHTS["PLAN_READY"]

    if state == "EXECUTE":
        cmd = entry.get("command","")
        if any(x in cmd for x in ["rm", "git reset", "drop", "delete"]):
            return RISK_WEIGHTS["EXECUTE_HIGH"]
        return RISK_WEIGHTS["EXECUTE_LOW"]

    return 0

def compute_maturity():
    if not LOG_FILE.exists():
        return 0.5

    data = json.loads(LOG_FILE.read_text())

    weighted_success = 0
    weighted_total = 0

    for entry in data:
        weight = classify_risk(entry)
        if weight == 0:
            continue

        weighted_total += weight
        if entry.get("success"):
            weighted_success += weight

    if weighted_total == 0:
        return 0.7

    return weighted_success / weighted_total

def dynamic_threshold():
    score = compute_maturity()

    if score >= 0.9:
        return 0.75
    elif score >= 0.8:
        return 0.85
    else:
        return 0.95
