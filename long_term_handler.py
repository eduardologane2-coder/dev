import json
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes

LONG_TERM_FILE = Path("/srv/dev/long_term_plan.json")

async def long_term_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not LONG_TERM_FILE.exists():
        await update.message.reply_text("Plano de longo prazo não encontrado.")
        return

    data = json.loads(LONG_TERM_FILE.read_text())

    vision = data.get("vision", "N/A")
    horizon = data.get("horizon_years", "N/A")
    milestones = data.get("milestones", [])
    last_review = data.get("last_review", "None")

    milestone_text = "\n".join(
        [f"- {m['id']} | {m['title']} | concluído: {m['completed']}" for m in milestones]
    )

    await update.message.reply_text(
        f"🌍 VISÃO:\n{vision}\n\n"
        f"📆 Horizonte: {horizon} anos\n\n"
        f"🎯 Milestones:\n{milestone_text}\n\n"
        f"Última revisão: {last_review}"
    )
