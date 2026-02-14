import json
from pathlib import Path

DEV_DIR = Path("/srv/dev")
STRATEGY_FILE = DEV_DIR / "strategy.json"

def detect_conflict(new_instruction):
    data = json.loads(STRATEGY_FILE.read_text())
    active_objective = data["objective_active"]["title"].lower()

    instruction = new_instruction.lower()

    # Exemplo simples de conflito estrutural
    if "apagar estratégia" in instruction:
        return True, "Instrução conflita com objetivo ativo."

    if "desativar autonomia" in instruction:
        return True, "Instrução conflita com meta estratégica."

    return False, None
