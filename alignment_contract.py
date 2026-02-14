import json
from pathlib import Path
from datetime import datetime

CONTRACT_FILE = Path("/srv/dev/joseph_contract.json")

def init_contract():
    if not CONTRACT_FILE.exists():
        CONTRACT_FILE.write_text(json.dumps({
            "joseph_objectives": [],
            "dev_objectives": [],
            "alignment_rules": [
                "Dev deve priorizar objetivos declarados por Joseph",
                "Dev não pode alterar objetivo ativo sem registro",
                "Dev deve validar impacto estratégico antes de execução crítica"
            ],
            "last_alignment_check": None
        }, indent=2))

def load_contract():
    init_contract()
    return json.loads(CONTRACT_FILE.read_text())

def save_contract(data):
    CONTRACT_FILE.write_text(json.dumps(data, indent=2))

def add_joseph_objective(title):
    data = load_contract()
    data["joseph_objectives"].append({
        "title": title,
        "created_at": str(datetime.now())
    })
    save_contract(data)

def alignment_status():
    data = load_contract()
    return {
        "joseph_objectives": len(data["joseph_objectives"]),
        "dev_objectives": len(data["dev_objectives"]),
        "rules": len(data["alignment_rules"])
    }
