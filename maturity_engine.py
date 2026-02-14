import json
from pathlib import Path

COGNITIVE_LOG = Path("/srv/dev/cognitive_log.json")

BASE_MIN = 0.3
BASE_MAX = 0.98

def load_log():
    if not COGNITIVE_LOG.exists():
        return []
    return json.loads(COGNITIVE_LOG.read_text())

def save_log(data):
    COGNITIVE_LOG.write_text(json.dumps(data, indent=2))

def compute_domain_maturity():
    data = load_log()

    domains = ["shell", "strategic", "git", "critical"]
    scores = {d: 0.7 for d in domains}

    for entry in data:
        domain = entry.get("domain")
        success = entry.get("success")
        critical = entry.get("critical", False)

        if domain not in scores:
            continue

        if success:
            scores[domain] += 0.02
        else:
            if critical:
                scores[domain] -= 0.15
            else:
                scores[domain] -= 0.03

    # clamp
    for d in scores:
        if scores[d] < BASE_MIN:
            scores[d] = BASE_MIN
        if scores[d] > BASE_MAX:
            scores[d] = BASE_MAX

    return scores

def dynamic_threshold(domain=None):
    scores = compute_domain_maturity()

    if domain is None:
        avg = sum(scores.values()) / len(scores)
    else:
        avg = scores.get(domain, 0.7)

    if avg < 0.6:
        return 0.97
    if avg < 0.8:
        return 0.95
    if avg < 0.9:
        return 0.90
    return 0.85

def register_execution(domain, success=True, critical=False):
    data = load_log()

    data.append({
        "domain": domain,
        "success": success,
        "critical": critical
    })

    save_log(data)
