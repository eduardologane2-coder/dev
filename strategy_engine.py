import json
from pathlib import Path
from datetime import datetime

DEV_DIR = Path("/srv/dev")
STRATEGY_FILE = DEV_DIR / "strategy.json"
STRATEGY_LOG = DEV_DIR / "strategy_log.json"

def detect_mode(text: str):
    text_lower = text.lower()

    planning_keywords = [
        "melhorar",
        "criar sistema",
        "arquitetura",
        "planejar",
        "estratégia",
        "evoluir",
        "reorganizar"
    ]

    analysis_keywords = [
        "analisar",
        "avaliar",
        "diagnosticar",
        "por que",
        "problema",
        "erro"
    ]

    for word in planning_keywords:
        if word in text_lower:
            return "modo_planejamento"

    for word in analysis_keywords:
        if word in text_lower:
            return "modo_analise"

    return "modo_execucao"


def log_strategy_decision(decision, reason, impact=None, commit=None):
    if not STRATEGY_LOG.exists():
        STRATEGY_LOG.write_text("[]")

    data = json.loads(STRATEGY_LOG.read_text())

    entry = {
        "timestamp": str(datetime.now()),
        "decision": decision,
        "reason": reason,
        "impact": impact,
        "commit": commit
    }

    data.append(entry)

    STRATEGY_LOG.write_text(json.dumps(data, indent=2))


def update_strategy_focus(mode):
    data = json.loads(STRATEGY_FILE.read_text())
    data["current_mode"] = mode
    data["last_update"] = str(datetime.now())
    STRATEGY_FILE.write_text(json.dumps(data, indent=2))
