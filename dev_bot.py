#!/usr/bin/env python3

import subprocess
import shutil
from pathlib import Path
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

from cognitive_engine import cognitive_decision
from human_renderer import render_human
from confidence_engine import can_auto_execute
from cognitive_log_engine import log_decision

REPO_DIR = Path("/srv/repo")
WORKSPACES_DIR = Path("/srv/workspaces")
ENV_FILE = Path("/srv/dev/.env")
AUTHORIZED_USER = 426824590

def load_token():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("TELEGRAM_TOKEN="):
            return line.split("=",1)[1].strip()
    raise RuntimeError("TELEGRAM_TOKEN não encontrado")

def create_workspace():
    WORKSPACES_DIR.mkdir(exist_ok=True)
    ws = WORKSPACES_DIR / f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    subprocess.run(["git","clone",str(REPO_DIR),str(ws)],stdout=subprocess.PIPE)
    return ws

def execute(cmd,cwd):
    result = subprocess.run(cmd,shell=True,cwd=cwd,capture_output=True,text=True)
    return result.returncode==0, result.stdout+result.stderr

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()

    decision = cognitive_decision(text)
    log_decision(decision)

    await update.message.reply_text(render_human(decision))

    if decision.get("state") != "EXECUTE":
        return

    if not can_auto_execute(decision):
        await update.message.reply_text(
            "Deseja executar este comando técnico?"
        )
        return

    await update.message.reply_text("⚙️ Executando comando supervisionado...")

    ws = create_workspace()
    success, output = execute(text, ws)

    shutil.rmtree(ws, ignore_errors=True)

    if success:
        await update.message.reply_text("✅ Execução concluída.")
    else:
        await update.message.reply_text("❌ Falha na execução.")

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - AUTONOMIA SUPERVISIONADA")
    app.run_polling()

if __name__ == "__main__":
    main()
