#!/usr/bin/env python3

import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

from cognitive_engine import cognitive_decision
from human_renderer import render_human
from confidence_gate import allow_execution
from context_lock import activate_briefing, deactivate_briefing, is_briefing_active

REPO_DIR = Path("/srv/dev")
WORKSPACES_DIR = REPO_DIR / "workspaces"

AUTHORIZED_USER = 426824590
EXECUTING = False

def load_token():
    with open("/srv/dev/.env") as f:
        for line in f:
            if line.startswith("TELEGRAM_TOKEN="):
                return line.split("=",1)[1].strip()
    raise RuntimeError("Token não encontrado")

def create_workspace():
    WORKSPACES_DIR.mkdir(exist_ok=True)
    ws = WORKSPACES_DIR / f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    subprocess.run(["git","clone",str(REPO_DIR),str(ws)],stdout=subprocess.PIPE)
    return ws

def execute(cmd,cwd):
    result = subprocess.run(cmd,shell=True,cwd=cwd,capture_output=True,text=True)
    return result.returncode==0, result.stdout+result.stderr

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global EXECUTING

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()

    decision = cognitive_decision(text)
    state = decision.get("state")

    # 🔒 CONTEXT LOCK
    if is_briefing_active() and state == "EXECUTE":
        await update.message.reply_text(
            "Você deseja interromper o briefing estratégico para executar um comando técnico?"
        )
        return

    # Humanização
    human_text = render_human(decision)
    await update.message.reply_text(human_text)

    # Ativar ou desativar briefing
    if state == "PLAN_READY":
        activate_briefing()
        return

    if state == "EXECUTE":
        deactivate_briefing()

    # Confidence gate
    if not allow_execution(decision):
        return

    if EXECUTING:
        await update.message.reply_text("Execução já em andamento.")
        return

    EXECUTING = True

    ws = create_workspace()
    success, output = execute(decision["plan"][0], ws)

    shutil.rmtree(ws, ignore_errors=True)

    if success:
        await update.message.reply_text("✅ Execução concluída.")
    else:
        await update.message.reply_text(f"❌ Falha:\n{output}")

    EXECUTING = False

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - COGNITIVE CORE V3")
    app.run_polling()

if __name__ == "__main__":
    main()
