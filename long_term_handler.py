import json
from telegram import Update
from telegram.ext import ContextTypes
from long_term_engine import review_plan, sync_with_evolution
from pathlib import Path

DEV_DIR = Path("/srv/dev")
PLAN_FILE = DEV_DIR / "long_term_plan.json"

async def longterm_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    review_plan()
    sync_with_evolution()

    plan = json.loads(PLAN_FILE.read_text())

    milestones = "\n".join(
        [f"- {m['id']} | {m['title']} | concluído: {m['completed']}"
         for m in plan["milestones"]]
    )

    await update.message.reply_text(
        f"🌍 VISÃO:\n{plan['vision']}\n\n"
        f"📆 Horizonte: {plan['horizon']}\n\n"
        f"🎯 Milestones:\n{milestones}\n\n"
        f"Última revisão: {plan['last_review']}"
    )
