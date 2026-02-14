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

from cognitive_metrics_engine import register_decision
from cognitive_metrics_handler import cognitive_metrics_status
from metrics_engine import metrics_status

BASE_DIR = Path("/srv/dev")
ENV_FILE = BASE_DIR / ".env"
REPO_DIR = BASE_DIR

AUTHORIZED_USER = 426824590
EXECUTING = False
PENDING_CMD = None


# ==========================
# ENV
# ==========================

def load_token():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("TELEGRAM_TOKEN="):
            return line.split("=",1)[1].strip()
    raise RuntimeError("TELEGRAM_TOKEN não encontrado")


# ==========================
# WORKSPACE
# ==========================

def create_workspace():
    ws = REPO_DIR / f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    subprocess.run(["git","clone",str(REPO_DIR),str(ws)],stdout=subprocess.PIPE)
    return ws


def execute(cmd,cwd):
    result = subprocess.run(cmd,shell=True,cwd=cwd,capture_output=True,text=True)
    return result.returncode==0, result.stdout+result.stderr


# ==========================
# HANDLER
# ==========================

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()

    # ==========================
    # COGNITIVE CORE
    # ==========================


    if not valid:
        await update.message.reply_text(f"❌ Erro cognitivo: {msg}")
        return



    if state == "PLAN":
        await update.message.reply_text("🧠 Plano estratégico gerado:")
        return

    if state == "REJECT":
        await update.message.reply_text("🚫 Instrução rejeitada.")
        return

    if state == "BRIEFING":
        return

    # ==========================
    # EXECUÇÃO
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

    if not success:
        shutil.rmtree(ws,ignore_errors=True)
        await update.message.reply_text(f"Falha:\n{output}")
        return

    await update.message.reply_text("Comando executado com sucesso.")
    shutil.rmtree(ws,ignore_errors=True)


# ==========================
# MAIN
# ==========================

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("metrics", lambda u, c: u.message.reply_text(metrics_status())))
    app.add_handler(CommandHandler("cognitive", lambda u, c: u.message.reply_text(cognitive_metrics_status())))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - CLEAN COGNITIVE CORE")
    app.run_polling()


if __name__ == "__main__":
    main()

# ==========================
# COMMAND HANDLER (COGNITIVE CLEAN)
# ==========================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global EXECUTING, PENDING_CMD

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()

    # ==========================
    # COGNITIVE CORE
    # ==========================

    decision = cognitive_decision(text)
    state = decision.get("state")

    if state == "PLAN":
        await update.message.reply_text("🧠 Preciso entender melhor antes de gerar plano.")
        await update.message.reply_text(decision.get("plan", ""))
        return

    if state == "BRIEFING":
        await update.message.reply_text(decision.get("message"))
        return

    if state == "CONFIRM":
        await update.message.reply_text("Confirmação recebida.")
        return

    if state != "EXECUTE":
        await update.message.reply_text("Estado cognitivo inválido.")
        return

    # ==========================
    # EXECUÇÃO CONTROLADA
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

    if not success:
        shutil.rmtree(ws, ignore_errors=True)
        await update.message.reply_text(f"Falha:\n{output}")
        await update.message.reply_text("Workspace destruído.")
        return

    subprocess.run(["cp", "-r", f"{ws}/.", str(REPO_DIR)])
    subprocess.run(["git", "add", "."], cwd=REPO_DIR)

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )

    if status.stdout.strip() == "":
        shutil.rmtree(ws, ignore_errors=True)
        await update.message.reply_text("Nenhuma alteração.")
        return

    subprocess.run(["git", "commit", "-m", f"auto(dev): {cmd}"], cwd=REPO_DIR)

    commit_hash = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO_DIR
    ).decode().strip()

    shutil.rmtree(ws, ignore_errors=True)

    await update.message.reply_text(f"Aplicado commit {commit_hash}")
    await update.message.reply_text("Workspace destruído.")

