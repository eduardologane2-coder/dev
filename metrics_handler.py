from telegram import Update
from telegram.ext import ContextTypes
from metrics_engine import get_metrics

async def metrics_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_metrics()
    await update.message.reply_text(
        f"📊 MÉTRICAS DO DEV\n\n"
        f"Execuções: {data['executions']}\n"
        f"Commits: {data['commits']}\n"
        f"SelfMods: {data['selfmods']}\n"
        f"Falhas: {data['failures']}\n"
        f"Rollbacks: {data['rollbacks']}\n"
        f"Última atualização: {data['last_update']}"
    )
