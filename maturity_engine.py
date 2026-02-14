import json
from pathlib import Path

LOG_FILE = Path("/srv/dev/cognitive_log.json")

DOMAINS = ["shell", "strategic", "git", "critical"]

RISK_WEIGHTS = {
    "shell": 2,
    "strategic": 1,
    "git": 3,
    "critical": 5
}

def classify_domain(entry):
    state = entry.get("state")

    if state == "PLAN_READY":
        return "strategic"

    if state == "EXECUTE":
        cmd = entry.get("command","").lower()

        if any(x in cmd for x in ["rm ", "drop ", "delete ", "truncate "]):
            return "critical"

        if "git" in cmd:
            return "git"

        return "shell"

    return None


def compute_domain_maturity():
    if not LOG_FILE.exists():
        return {d: 0.7 for d in DOMAINS}

    data = json.loads(LOG_FILE.read_text())

    scores = {}
    for domain in DOMAINS:
        weighted_success = 0
        weighted_total = 0

        for entry in data:
            entry_domain = classify_domain(entry)
            if entry_domain != domain:
                continue

            weight = RISK_WEIGHTS.get(domain,1)
            weighted_total += weight

            if entry.get("success"):
                weighted_success += weight

        if weighted_total == 0:
            scores[domain] = 0.7
        else:
            scores[domain] = weighted_success / weighted_total

    return scores


def dynamic_threshold(domain):
    scores = compute_domain_maturity()
    score = scores.get(domain,0.7)

    if score >= 0.9:
        return 0.75
    elif score >= 0.8:
        return 0.85
    else:
        return 0.95
