#!/usr/bin/env python3

import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from cognitive_engine import cognitive_decision

BASE_DIR = Path("/srv/dev")
REPO_DIR = BASE_DIR
WORKSPACES_DIR = BASE_DIR / "workspace"
ENV_FILE = BASE_DIR / ".env"

AUTHORIZED_USER = 426824590

EXECUTING = False
PENDING_CMD = None


def load_token():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("TELEGRAM_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("TELEGRAM_TOKEN não encontrado")


def create_workspace():
    WORKSPACES_DIR.mkdir(exist_ok=True)
    ws = WORKSPACES_DIR / f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    subprocess.run(["git", "clone", str(REPO_DIR), str(ws)], stdout=subprocess.PIPE)
    return ws


def execute(cmd, cwd):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr


# ==========================
# HANDLE
# ==========================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PENDING_CMD

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()

    decision = cognitive_decision(text)
    state = decision.get("state")

    # -------- BRIEFING --------
    if state == "BRIEFING":
        await update.message.reply_text(decision.get("message"))
        return

    # -------- PLANO --------
    if state == "PLAN":
        await update.message.reply_text("🧠 Plano gerado:")
        await update.message.reply_text(decision.get("plan"))
        return

    # -------- EXECUÇÃO --------
    if state != "EXECUTE":
        await update.message.reply_text("Estado cognitivo inválido.")
        return

    if PENDING_CMD is None:
        PENDING_CMD = text
        await update.message.reply_text(f"Proposta:\n\n{text}\n\nExecutar? (sim)")
        return

    if text.lower() != "sim":
        await update.message.reply_text("Cancelado.")
        PENDING_CMD = None
        return

    cmd = PENDING_CMD
    PENDING_CMD = None

    await update.message.reply_text("Criando workspace...")
    ws = create_workspace()

    await update.message.reply_text("Executando...")
    success, output = execute(cmd, ws)

    if not success:
        shutil.rmtree(ws, ignore_errors=True)
        await update.message.reply_text(f"Falha:\n{output}")
        await update.message.reply_text("Workspace destruído.")
        return

    shutil.rmtree(ws, ignore_errors=True)

    await update.message.reply_text("Execução concluída.")


def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - CLEAN COGNITIVE CORE")
    app.run_polling()


if __name__ == "__main__":
    main()
