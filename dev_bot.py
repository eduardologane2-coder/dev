from briefing_engine import start_briefing, append_input, load_state, close_briefing
#!/usr/bin/env python3

import json
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

from cognitive_engine import cognitive_decision
from llm_engine import ask_llm

REPO_DIR = Path("/srv/repo")
WORKSPACES_DIR = Path("/srv/dev/workspaces")
ENV_FILE = Path("/srv/dev/.env")

AUTHORIZED_USER = 426824590
PENDING_CMD = None


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


def execute(cmd, cwd):
    result = subprocess.run(cmd,shell=True,cwd=cwd,capture_output=True,text=True)
    return result.returncode==0, result.stdout+result.stderr


    token = load_token()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - CLEAN COGNITIVE CORE")
    app.run_polling()


if __name__ == "__main__":
    main()
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PENDING_CMD

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()

    from cognitive_engine import cognitive_decision
    from cognitive_validator import validate_decision

    decision = cognitive_decision(text)
    valid, msg = validate_decision(decision)

    if not valid:
        await update.message.reply_text(f"Erro estrutural: {msg}")
        return

    state = decision["state"]
    confidence = decision["confidence"]

    briefing = load_state()

    # -------- BRIEFING ITERATIVO --------
    if briefing["active"]:
        append_input(text)
        await update.message.reply_text("Continuando briefing...")
        return

    if state == "BRIEFING":
        start_briefing(text)
        await update.message.reply_text(decision.get("message"))
        return

    # -------- PLANO --------
    if state == "PLAN_READY":
        if confidence < 0.7:
            await update.message.reply_text("Plano gerado, mas com baixa confiança. Deseja revisar?")
            await update.message.reply_text(decision.get("plan"))
            return

        await update.message.reply_text("Plano estruturado:")
        await update.message.reply_text(decision.get("plan"))
        return

    # -------- EXECUÇÃO --------
    if state == "EXECUTE":
        PENDING_CMD = text
        await update.message.reply_text(f"Executar comando técnico?\n{text}")
        return


# ==========================
# MAIN
# ==========================

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - CLEAN COGNITIVE CORE")
    app.run_polling()


if __name__ == "__main__":
    main()

