#!/usr/bin/env python3

import os
import json
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

from metrics_engine import inc, metrics_status
from alignment_handler import alignment_status_handler
from long_term_handler import long_term_status_handler
from cognitive_engine import cognitive_decision
from plan_validator import validate_plan
from plan_executor import execute_plan


BASE_DIR = Path("/srv/dev")
ENV_FILE = BASE_DIR / ".env"
REPO_DIR = BASE_DIR
WORKSPACES_DIR = BASE_DIR / "workspace"

AUTHORIZED_USER = 426824590
EXECUTING = False
PENDING_CMD = None


# ==========================
# UTIL
# ==========================

def load_token():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("TELEGRAM_TOKEN="):
            return line.split("=",1)[1].strip()
    raise RuntimeError("TELEGRAM_TOKEN não encontrado")


def create_workspace():
    WORKSPACES_DIR.mkdir(exist_ok=True)
    ws = WORKSPACES_DIR / f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    subprocess.run(["git","clone",str(REPO_DIR),str(ws)], stdout=subprocess.PIPE)
    return ws


def execute(cmd, cwd):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr


# ==========================
# HANDLER PRINCIPAL
# ==========================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global EXECUTING, PENDING_CMD

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()


    state, justification = cognitive_decision(text)



    if state == "PLAN":

        await update.message.reply_text("🧠 Plano estratégico gerado:")

        await update.message.reply_text(justification)

        return



    if state == "REJECT":

        await update.message.reply_text("🚫 Instrução rejeitada.")

        await update.message.reply_text(justification)

        return



        await update.message.reply_text("❌ Instrução rejeitada pelo núcleo estratégico.")
        return

    # ==========================
    # EXECUÇÃO NORMAL
    # ==========================

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
    inc("executions")

    if not success:
        shutil.rmtree(ws, ignore_errors=True)
        inc("failures")
        await update.message.reply_text(f"Falha:\n{output}")
        return

    subprocess.run(["cp","-r",f"{ws}/.",str(REPO_DIR)])
    subprocess.run(["git","add","."],cwd=REPO_DIR)

    status = subprocess.run(["git","status","--porcelain"],cwd=REPO_DIR,capture_output=True,text=True)

    if status.stdout.strip()=="":
        shutil.rmtree(ws,ignore_errors=True)
        await update.message.reply_text("Nenhuma alteração.")
        return

    commit_msg=f"auto(dev): {cmd}"
    subprocess.run(["git","commit","-m",commit_msg],cwd=REPO_DIR)
    inc("commits")

    commit_hash=subprocess.check_output(["git","rev-parse","--short","HEAD"],cwd=REPO_DIR).decode().strip()

    shutil.rmtree(ws,ignore_errors=True)

    await update.message.reply_text(f"Aplicado commit {commit_hash}")


# ==========================
# MAIN
# ==========================

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("metrics", lambda u,c: u.message.reply_text(metrics_status())))
    app.add_handler(CommandHandler("alignment", alignment_status_handler))
    app.add_handler(CommandHandler("longterm", long_term_status_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - CLEAN COGNITIVE CORE")
    app.run_polling()


if __name__ == "__main__":
    main()
