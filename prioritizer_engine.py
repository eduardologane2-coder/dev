import json
from pathlib import Path

DEV_DIR = Path("/srv/dev")
STRATEGY_FILE = DEV_DIR / "strategy.json"

def calculate_priority_score(task):
    impact = task.get("impact", 1)
    urgency = task.get("urgency", 1)
    risk = task.get("risk", 1)

    # Impacto e urgência aumentam prioridade
    # Risco reduz prioridade
    return (impact * 2 + urgency) - risk

def prioritize_tasks():
    data = json.loads(STRATEGY_FILE.read_text())

    tasks = data.get("open_tasks", [])

    scored = []
    for t in tasks:
        score = calculate_priority_score(t)
        scored.append((score, t))

    scored.sort(reverse=True, key=lambda x: x[0])

    ordered = [t for score, t in scored]

    data["open_tasks"] = ordered
    STRATEGY_FILE.write_text(json.dumps(data, indent=2))

    return ordered
