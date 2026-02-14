import json
from pathlib import Path
from datetime import datetime

DEV_PATH = Path("/srv/dev")
CONTRACT_FILE = DEV_PATH / "alignment_contract.json"
LOG_FILE = DEV_PATH / "alignment_log.json"

def load_contract():
    if not CONTRACT_FILE.exists():
        return {
            "joseph_objectives": [],
            "dev_objectives": [],
            "rules": [
                "Dev não pode violar objetivo ativo de Joseph.",
                "Dev deve priorizar estabilidade antes de expansão.",
                "Conflitos devem ser explicitamente confirmados."
            ]
        }
    return json.loads(CONTRACT_FILE.read_text())

def save_contract(data):
    CONTRACT_FILE.write_text(json.dumps(data, indent=2))

def log_alignment(event):
    logs = []
    if LOG_FILE.exists():
        logs = json.loads(LOG_FILE.read_text())
    logs.append(event)
    LOG_FILE.write_text(json.dumps(logs, indent=2))

def check_alignment(instruction):
    data = load_contract()
    active = [o["title"] for o in data["joseph_objectives"]]

    for obj in active:
        if "apagar" in instruction.lower() and obj.lower() in instruction.lower():
            return False, "Instrução conflita com objetivo Joseph."

    return True, None

def add_joseph_objective(title, weight=1.0):
    data = load_contract()
    data["joseph_objectives"].append({
        "title": title,
        "weight": weight,
        "created_at": str(datetime.now())
    })
    save_contract(data)

def add_dev_objective(title):
    data = load_contract()
    data["dev_objectives"].append({
        "title": title,
        "created_at": str(datetime.now())
    })
    save_contract(data)
