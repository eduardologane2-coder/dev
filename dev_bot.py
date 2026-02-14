#!/usr/bin/env python3

import json
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
from context_lock_engine import load_state, activate, deactivate
from cognitive_score_engine import increase, decrease, get_score
from context_shift_engine import detect_shift
from briefing_history_engine import append_entry
from dominant_intent_engine import tracker

ENV_FILE = Path("/srv/dev/.env")
WORKSPACES_DIR = Path("/srv/dev/workspaces")
AUTHORIZED_USER = 426824590

def load_token():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("TELEGRAM_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("TELEGRAM_TOKEN não encontrado")

def create_workspace():
    WORKSPACES_DIR.mkdir(exist_ok=True)
    ws = WORKSPACES_DIR / f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    subprocess.run(["mkdir", str(ws)])
    return ws

def execute(cmd, cwd):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()
    decision = cognitive_decision(text)
    state = decision.get("state")

    tracker.add(state)

    lock = load_state()

    if lock.get("active"):
        shifted = detect_shift(lock.get("topic"), text)
        if shifted:
            await update.message.reply_text("Detectei mudança de contexto.")
        else:
            increase(1)

    if state == "PLAN_READY":
        activate(text)
        increase(2)
        append_entry(text, get_score())

        plan = decision.get("plan")
        if isinstance(plan, dict):
            plan = json.dumps(plan, indent=2)

        await update.message.reply_text("🧠 Plano estruturado:\n")
        await update.message.reply_text(plan)
        return

    if state != "EXECUTE":
        await update.message.reply_text("Estado cognitivo inválido.")
        return

    ws = create_workspace()
    success, output = execute(text, ws)

    if not success:
        shutil.rmtree(ws, ignore_errors=True)
        decrease(1)
        await update.message.reply_text(f"Falha:\n{output}")
        return

    shutil.rmtree(ws, ignore_errors=True)
    increase(1)
    await update.message.reply_text("Execução concluída.")

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - COGNITIVE CORE LEVEL 4")
    app.run_polling()

if __name__ == "__main__":
    main()
