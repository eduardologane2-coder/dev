from alignment_contract import load_contract
from datetime import datetime
import json
from pathlib import Path

STRATEGY_FILE = Path("/srv/dev/strategy.json")

def validate_alignment(command_text):
    contract = load_contract()
    strategy = json.loads(STRATEGY_FILE.read_text())

    objective = strategy.get("objective_active", {}).get("title", "")

    if "apagar estratégia" in command_text.lower():
        return False, "Comando conflita com objetivo estratégico ativo."

    if len(contract["joseph_objectives"]) == 0:
        return True, "Nenhum objetivo explícito de Joseph definido."

    return True, "Alinhamento válido."

def register_alignment_check():
    contract = load_contract()
    contract["last_alignment_check"] = str(datetime.now())
    from alignment_contract import save_contract
    save_contract(contract)
