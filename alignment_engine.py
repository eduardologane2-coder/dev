import json
from pathlib import Path
from datetime import datetime

CONTRACT_FILE = Path("/srv/dev/alignment_contract.json")
LOG_FILE = Path("/srv/dev/alignment_log.json")

def load_contract():
    if not CONTRACT_FILE.exists():
        return {"joseph_objectives": [], "dev_objectives": [], "rules": []}
    return json.loads(CONTRACT_FILE.read_text())

def save_contract(data):
    CONTRACT_FILE.write_text(json.dumps(data, indent=2))

def register_alignment_check(instruction, result):
    log = []
    if LOG_FILE.exists():
        log = json.loads(LOG_FILE.read_text())
    log.append({
        "timestamp": str(datetime.now()),
        "instruction": instruction,
        "result": result
    })
    LOG_FILE.write_text(json.dumps(log, indent=2))

def validate_alignment(instruction):
    contract = load_contract()
    rules = contract.get("rules", [])

    for rule in rules:
        if rule.lower() in instruction.lower():
            return False, f"Instrução viola regra: {rule}"

    return True, "Alinhado com contrato."
