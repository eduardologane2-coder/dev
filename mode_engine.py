import json
from pathlib import Path
from datetime import datetime

STRATEGY_FILE = Path("/srv/dev/strategy.json")

PLANNING_KEYWORDS = [
    "estratégia",
    "planejar",
    "arquitetura",
    "melhorar",
    "evoluir",
    "refatorar"
]

ANALYSIS_KEYWORDS = [
    "analisar",
    "avaliar",
    "diagnosticar",
    "revisar",
    "verificar"
]

def detect_mode(text: str) -> str:
    lower = text.lower()

    if any(k in lower for k in PLANNING_KEYWORDS):
        return "modo_planejamento"

    if any(k in lower for k in ANALYSIS_KEYWORDS):
        return "modo_analise"

    return "modo_execucao"


def persist_mode(mode: str):
    if not STRATEGY_FILE.exists():
        return

    data = json.loads(STRATEGY_FILE.read_text())
    data["current_mode"] = mode
    data["last_update"] = str(datetime.now())
    STRATEGY_FILE.write_text(json.dumps(data, indent=2))
