import os
from pathlib import Path

DEV_PATH = Path("/srv/dev")

REQUIRED_FILES = [
    "dev_bot.py",
    "evolution_engine.py",
    "selfmod_engine.py",
    "metrics_engine.py",
]

def run_integrity_checks():
    missing = []
    for f in REQUIRED_FILES:
        if not (DEV_PATH / f).exists():
            missing.append(f)

    if missing:
        return False, f"Arquivos obrigatórios ausentes: {missing}"

    return True, "Integridade estrutural OK"


# === STAGE EVOLUTION (mantido) ===

def get_stage(data):
    return data.get("evolution_stage", "bootstrap")


def transition_stage(data):
    stage = get_stage(data)

    if stage == "bootstrap":
        data["evolution_stage"] = "strategic"
    elif stage == "strategic":
        data["evolution_stage"] = "architectural"
    elif stage == "architectural":
        data["evolution_stage"] = "cognitive"

    return data
