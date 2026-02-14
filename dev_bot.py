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

from llm_engine import ask_llm
from strategy_llm_engine import evaluate_strategy
from cognitive_engine import cognitive_decision
from metrics_engine import inc, metrics_status
from alignment_engine import validate_alignment
from selfmod_engine import is_self_mod_command, apply_self_mod

# ==========================
# CONFIG
# ==========================

DEV_DIR = Path("/srv/dev")
REPO_DIR = Path("/srv/repo")
WORKSPACES_DIR = Path("/srv/workspaces")
ENV_FILE = DEV_DIR / ".env"

AUTHORIZED_USER = 426824590

EXECUTING = False
PENDING_CMD = None

# ==========================
# ENV
# ==========================

def load_token():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("TELEGRAM_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("TELEGRAM_TOKEN não encontrado")

# ==========================
# MODE ENGINE
# ==========================

def detect_mode(text):
    decision, explanation = evaluate_strategy(text)
    return decision, explanation

# ==========================
# WORKSPACE
# ==========================

def create_workspace():
    WORKSPACES_DIR.mkdir(exist_ok=True)
    ws = WORKSPACES_DIR / f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    subprocess.run(["git", "clone", str(REPO_DIR), str(ws)], stdout=subprocess.PIPE)
    return ws

def execute(cmd, cwd):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr

# ==========================
# COMMAND HANDLER
# ==========================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global EXECUTING, PENDING_CMD

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()

    # ==========================
    # COGNITIVE DECISION ENGINE
    # ==========================
    decision_data = cognitive_decision(text)
    decision = decision_data.get("decision")

    if decision == "REJECT":
        await update.message.reply_text(f"❌ REJEITADO: {decision_data.get('reason')}")
        return

    if decision == "PLAN":
        plan_steps = "\n".join([f"- {p}" for p in decision_data.get("plan", [])])
        await update.message.reply_text("🧠 Plano estratégico gerado:")
        await update.message.reply_text(plan_steps)
        return


    # ==========================
    # ALIGNMENT CHECK
    # ==========================
    ok, align_msg = validate_alignment(text)
    if not ok:
        await update.message.reply_text(f"⚠️ Violação de alinhamento:\n{align_msg}")
        return

    # ==========================
    # STRATEGY DECISION
    # ==========================
    decision, explanation = detect_mode(text)

    if decision == "PLAN":
        await update.message.reply_text("🧠 Gerando plano estratégico via LLM...")
        plan = ask_llm(text)
        await update.message.reply_text(plan)
        return

    if decision == "REJECT":
        await update.message.reply_text("❌ Instrução rejeitada estrategicamente.")
        await update.message.reply_text(explanation)
        return

    # ==========================
    # EXECUTION FLOW
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

    if EXECUTING:
        await update.message.reply_text("Execução já em andamento.")
        return

    EXECUTING = True

    # ==========================
    # SELF-MOD
    # ==========================
    if is_self_mod_command(cmd):
        await update.message.reply_text("🛠 Detectado comando de self-modificação.")
        ok, result = apply_self_mod(cmd)
        if ok:
            inc("selfmods")
            await update.message.reply_text(result)
        else:
            inc("rollbacks")
            await update.message.reply_text("❌ Self-mod falhou. Rollback executado.")
            await update.message.reply_text(result)
        EXECUTING = False
        return

    await update.message.reply_text("Criando workspace...")
    ws = create_workspace()

    await update.message.reply_text("Executando...")
    success, output = execute(cmd, ws)
    inc("executions")

    if not success:
        shutil.rmtree(ws, ignore_errors=True)
        inc("failures")
        await update.message.reply_text(f"Falha:\n{output}")
        EXECUTING = False
        return

    subprocess.run(["cp", "-r", f"{ws}/.", str(REPO_DIR)])
    subprocess.run(["git", "add", "."], cwd=REPO_DIR)

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )

    if status.stdout.strip() == "":
        shutil.rmtree(ws, ignore_errors=True)
        await update.message.reply_text("Nenhuma alteração.")
        EXECUTING = False
        return

    commit_msg = f"auto(dev): {cmd}"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_DIR)
    inc("commits")

    commit_hash = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO_DIR,
    ).decode().strip()

    shutil.rmtree(ws, ignore_errors=True)

    await update.message.reply_text(f"Aplicado commit {commit_hash}")
    EXECUTING = False

# ==========================
# MAIN
# ==========================


# ==========================
# MAIN
# ==========================

from _main_patch import register_handlers

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()
    register_handlers(app, handle)
    print("DEV BOT ONLINE - CORE ESTÁVEL")
    app.run_polling()

if __name__ == "__main__":
    main()
