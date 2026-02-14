import json
from pathlib import Path
from alignment_engine import load_contract

CONTRACT_FILE = Path("/srv/dev/alignment_contract.json")

async def alignment_status(update, context):
    data = load_contract()

    joseph = len(data["joseph_objectives"])
    dev = len(data["dev_objectives"])
    rules = len(data["rules"])

    await update.message.reply_text(
        f"🔐 CONTRATO JOSEPH ↔ DEV\n\n"
        f"Objetivos Joseph: {joseph}\n"
        f"Objetivos Dev: {dev}\n"
        f"Regras de alinhamento: {rules}"
    )
