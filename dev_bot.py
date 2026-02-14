from llm_planner import generate_plan
from mode_engine import detect_mode, persist_mode
from llm_engine import llm_propose
from long_term_handler import long_term_status_handler
from long_term_handler import long_term_status_handler
from alignment_handler import alignment_status
from alignment_engine import check_alignment
from metrics_handler import metrics_status
from alignment_handler import alignment_status
#!/usr/bin/env python3

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

from metrics_engine import inc
from selfmod_engine import is_self_mod_command, apply_self_mod

# ==========================
# CONFIG
# ==========================

DEV_DIR = Path("/srv/dev")
REPO_DIR = Path("/srv/repo")
WORKSPACES_DIR = Path("/srv/workspaces")
STRATEGY_FILE = DEV_DIR / "strategy.json"

AUTHORIZED_USER = 426824590

EXECUTING = False
PENDING_CMD = None

# ==========================
# UTIL
# ==========================

def validate_repo():
    try:
        subprocess.check_output(["git","rev-parse","--is-inside-work-tree"],cwd=REPO_DIR)
        return True
    except:
        return False

def load_token():
    env = DEV_DIR / ".env"
    for line in env.read_text().splitlines():
        if line.startswith("TELEGRAM_TOKEN="):
            return line.split("=",1)[1].strip()
    raise RuntimeError("TOKEN não encontrado")

def create_workspace():
    WORKSPACES_DIR.mkdir(exist_ok=True)
    ws = WORKSPACES_DIR / f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    subprocess.run(["git","clone",str(REPO_DIR),str(ws)],stdout=subprocess.PIPE)
    return ws

def execute(cmd, cwd):
    result = subprocess.run(cmd,shell=True,cwd=cwd,capture_output=True,text=True)
    return result.returncode==0, result.stdout+result.stderr

# ==========================
# STRATEGY
# ==========================

async def strategy_status(update:Update,context:ContextTypes.DEFAULT_TYPE):
    data = json.loads(STRATEGY_FILE.read_text())
    await update.message.reply_text(
        f"OBJETIVO: {data['objective_active']['title']}\n"
        f"MODO: {data['current_mode']}\n"
        f"EVOLUTION: {data['evolution_stage']}"
    )

# ==========================
# HANDLER
# ==========================

async def handle(update:Update,context:ContextTypes.DEFAULT_TYPE):
    global EXECUTING, PENDING_CMD

    if update.effective_user.id!=AUTHORIZED_USER:
    return

    text = update.message.text.strip()
    mode = detect_mode(text)

    if mode == "modo_planejamento":
        await update.message.reply_text("🧠 Gerando plano estratégico via LLM...")
        plan = generate_plan(text)
        await update.message.reply_text(plan)
        return
    return

    if mode == "modo_analise":
        await update.message.reply_text("🔎 Entrando em modo ANÁLISE automática.")
    return
    if PENDING_CMD is None:
        PENDING_CMD=text
        await update.message.reply_text(f"Proposta:\n\n{text}\n\nExecutar? (sim)")
    return

    # Cancelamento
    if text.lower()!="sim":
        await update.message.reply_text("Cancelado.")
        PENDING_CMD=None
    return

    cmd=PENDING_CMD
    PENDING_CMD=None

    # Self-mod intercept
    if is_self_mod_command(cmd):
        await update.message.reply_text("🛠 Self-mod detectado.")
        ok,msg = apply_self_mod(cmd)
        if ok:
            inc("selfmods")
            await update.message.reply_text(msg)
        else:
            inc("rollbacks")
            await update.message.reply_text(msg)
    return

    if EXECUTING:
        await update.message.reply_text("Execução já em andamento.")
    return

    EXECUTING=True

    if not validate_repo():
        await update.message.reply_text("Repo inválido.")
        EXECUTING=False
    return

    await update.message.reply_text("Criando workspace...")
    ws=create_workspace()

    await update.message.reply_text("Executando...")
    success,output = execute(cmd,ws)
    inc("executions")

    if not success:
        shutil.rmtree(ws,ignore_errors=True)
        inc("failures")
        await update.message.reply_text(f"Falha:\n{output}")
        await update.message.reply_text("Workspace destruído.")
        EXECUTING=False
    return

    subprocess.run(["cp","-r",f"{ws}/.",str(REPO_DIR)])
    subprocess.run(["git","add","."],cwd=REPO_DIR)

    status=subprocess.run(["git","status","--porcelain"],cwd=REPO_DIR,capture_output=True,text=True)

    if status.stdout.strip()=="":
        shutil.rmtree(ws,ignore_errors=True)
        await update.message.reply_text("Nenhuma alteração.")
        EXECUTING=False
    return

    commit_msg=f"auto(dev): {cmd}"
    subprocess.run(["git","commit","-m",commit_msg],cwd=REPO_DIR)
    inc("commits")

    commit_hash=subprocess.check_output(["git","rev-parse","--short","HEAD"],cwd=REPO_DIR).decode().strip()

    shutil.rmtree(ws,ignore_errors=True)

    await update.message.reply_text(f"Aplicado commit {commit_hash}")
    await update.message.reply_text("Workspace destruído.")

    EXECUTING=False

# ==========================
# MAIN
# ==========================

def main():
    token=load_token()
    app=ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("longterm", long_term_status_handler))
    app.add_handler(CommandHandler("strategy",strategy_status))
    app.add_handler(CommandHandler("metrics", lambda u,c: u.message.reply_text(metrics_status())))
    app.add_handler(CommandHandler("alignment", alignment_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle))
    app.add_handler(CommandHandler("alignment", alignment_status))

    print("DEV BOT ONLINE - REBUILT CORE")
    app.run_polling()

if __name__=="__main__":
    main()

# === ALIGNMENT CHECK ===
try:
    from alignment_engine import validate_alignment, register_alignment_check
except:
    pass
