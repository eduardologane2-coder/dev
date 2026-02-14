import json
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes

CONTRACT_FILE = Path("/srv/dev/alignment_contract.json")

async def alignment_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not CONTRACT_FILE.exists():
        await update.message.reply_text("Contrato não encontrado.")
        return

    data = json.loads(CONTRACT_FILE.read_text())

    joseph_goals = len(data.get("joseph_objectives", []))
    dev_goals = len(data.get("dev_objectives", []))
    rules = len(data.get("alignment_rules", []))

    await update.message.reply_text(
        "🔐 CONTRATO JOSEPH ↔ DEV\n\n"
        f"Objetivos Joseph: {joseph_goals}\n"
        f"Objetivos Dev: {dev_goals}\n"
        f"Regras de alinhamento: {rules}"
    )
