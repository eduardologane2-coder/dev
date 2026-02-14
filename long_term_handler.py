from telegram import Update
from telegram.ext import ContextTypes
import json
from pathlib import Path

PLAN_FILE = Path("/srv/dev/long_term_plan.json")

async def longterm_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(PLAN_FILE.read_text())

    milestones = "\n".join([
        f"- {m['id']} | {m['title']} | concluído: {m['completed']}"
        for m in data["milestones"]
    ])

    await update.message.reply_text(
        f"🌍 VISÃO:\n{data['vision']}\n\n"
        f"📆 Horizonte: {data['horizon_years']} anos\n\n"
        f"🎯 Milestones:\n{milestones}\n\n"
        f"Última revisão: {data['last_review']}"
    )
