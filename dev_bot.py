from strategy_llm_engine import evaluate_strategy
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

# ==========================
# CONFIG
# ==========================

DEV_DIR = Path("/srv/dev")
REPO_DIR = Path("/srv/repo")
WORKSPACES_DIR = Path("/srv/workspaces")
ENV_FILE = DEV_DIR / ".env"
STRATEGY_FILE = DEV_DIR / "strategy.json"

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
# LLM ENGINE
# ==========================

def load_llm_key():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("OPENAI_API_KEY="):
            return line.split("=",1)[1].strip()
    return None

def generate_plan(text):
    key = load_llm_key()
    if not key:

    try:
# ==========================


# ==========================
# COMMAND HANDLER
# ==========================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global EXECUTING, PENDING_CMD

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()
    mode = detect_mode(text)

    # === MODO PLANEJAMENTO (LLM) ===
    if mode == "modo_planejamento":
        await update.message.reply_text("🧠 Gerando plano estratégico via LLM...")
        plan = generate_plan(text)
        await update.message.reply_text(plan)
        return

    # === MODO EXECUÇÃO ===
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
        await update.message.reply_text("Workspace destruído.")
        return

    commit_msg = f"auto(dev): {cmd}"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_DIR)

    commit_hash = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO_DIR
    ).decode().strip()

    shutil.rmtree(ws, ignore_errors=True)

    await update.message.reply_text(f"Aplicado commit {commit_hash}")
    await update.message.reply_text("Workspace destruído.")


# ==========================
# MAIN
# ==========================

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - LLM INTEGRATED CORE")
    app.run_polling()


if __name__ == "__main__":
    main()

