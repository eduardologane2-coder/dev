from telegram import Update
from telegram.ext import ContextTypes
from alignment_contract import alignment_status

async def alignment_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = alignment_status()

    await update.message.reply_text(
        f"🔐 CONTRATO JOSEPH ↔ DEV\n\n"
        f"Objetivos Joseph: {status['joseph_objectives']}\n"
        f"Objetivos Dev: {status['dev_objectives']}\n"
        f"Regras de alinhamento: {status['rules']}"
    )
