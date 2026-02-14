import json
from telegram import Update
from telegram.ext import ContextTypes
from pathlib import Path

DEV_DIR = Path("/srv/dev")
METRICS_FILE = DEV_DIR / "metrics.json"

async def metrics_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not METRICS_FILE.exists():
        await update.message.reply_text("Métricas ainda não iniciadas.")
        return

    data = json.loads(METRICS_FILE.read_text())

    msg = (
        f"📊 MÉTRICAS DO DEV\n\n"
        f"Execuções: {data['executions']}\n"
        f"Commits: {data['commits']}\n"
        f"SelfMods: {data['selfmods']}\n"
        f"Falhas: {data['failures']}\n"
        f"Rollbacks: {data['rollbacks']}\n"
        f"Última atualização: {data['last_update']}"
    )

    await update.message.reply_text(msg)
