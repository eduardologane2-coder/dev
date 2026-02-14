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
from context_lock_engine import (
    load_state,
    activate,
    deactivate,
    escalate_confidence,
    interpret_abort_response,
    can_auto_execute,
    requires_hard_confirmation,
)

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

    state = load_state()

    # ==========================
    # CONTEXT LOCK
    # ==========================
    if state["active"]:

        decision = cognitive_decision(text)

        if decision.get("state") == "EXECUTE":

            if not can_auto_execute():
                interpretation = interpret_abort_response(text)

                if interpretation == "CONTINUE_BRIEFING":
                    await update.message.reply_text("Seguimos no briefing estratégico.")
                    return

                if interpretation == "CONVERT_TO_PLAN":
                    await update.message.reply_text("Integrando como parte do plano.")
                    escalate_confidence()
                    return

                if interpretation == "ABORT_AND_EXECUTE":
                    if requires_hard_confirmation():
                        await update.message.reply_text(
                            "Estamos em estágio avançado do briefing. Confirme explicitamente que deseja abortar."
                        )
                        return
                    deactivate()
                    await update.message.reply_text("Abortando briefing. Executando comando.")
                else:
                    await update.message.reply_text(
                        "Você deseja interromper o briefing estratégico para executar um comando técnico?"
                    )
                    return
            else:
                deactivate()
                await update.message.reply_text("Confiança suficiente. Executando automaticamente.")

    # ==========================
    # COGNITIVE CORE
    # ==========================
    decision = cognitive_decision(text)
    state_name = decision.get("state")

    if state_name == "PLAN_READY":
        activate(text)
        escalate_confidence()
        plan = decision.get("plan")

        if isinstance(plan, dict):
            plan = json.dumps(plan, indent=2)

        await update.message.reply_text("🧠 Plano estruturado:\n")
        await update.message.reply_text(plan)
        return

    if state_name != "EXECUTE":
        await update.message.reply_text("Estado cognitivo inválido.")
        return

    # ==========================
    # EXECUÇÃO
    # ==========================
    ws = create_workspace()
    success, output = execute(text, ws)

    if not success:
        shutil.rmtree(ws, ignore_errors=True)
        await update.message.reply_text(f"Falha:\n{output}")
        return

    shutil.rmtree(ws, ignore_errors=True)
    await update.message.reply_text("Execução concluída.")

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("DEV BOT ONLINE - CONFIDENCE GATED CORE")
    app.run_polling()

if __name__ == "__main__":
    main()
