#!/usr/bin/env python3
from self_mod_engine import is_self_modification, create_branch, validate_syntax, run_tests, rollback
from strategy_engine import detect_mode, log_strategy_decision, update_strategy_focus

import subprocess
import shutil
import json
from datetime import datetime
from pathlib import Path

# === SELF-MOD IMPORTS ===
from selfmod_engine import create_selfmod_branch, rollback
from selfmod_validator import validate_python_file

def is_self_mod_command(cmd):
    return "/srv/dev/dev_bot.py" in cmd

def apply_self_mod(cmd):
    try:
        branch = create_selfmod_branch()
        subprocess.run(cmd, shell=True)

        ok, error = validate_python_file(Path("/srv/dev/dev_bot.py"))
        if not ok:
            rollback()
            return False, error

        subprocess.run(["git", "add", "dev_bot.py"], cwd="/srv/dev")
        subprocess.run(["git", "commit", "-m", f"selfmod: {cmd}"], cwd="/srv/dev")
        subprocess.run(["git", "checkout", "main"], cwd="/srv/dev")
        subprocess.run(["git", "merge", branch], cwd="/srv/dev")

        return True, f"Self-mod aplicado com sucesso via branch {branch}"

    except Exception as e:
        rollback()
        return False, str(e)

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# ==========================
# CONFIG
# ==========================

DEV_DIR = Path("/srv/dev")
REPO_DIR = Path("/srv/repo")
WORKSPACES_DIR = Path("/srv/workspaces")
LOG_FILE = DEV_DIR / "dev_exec.log"
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
    raise RuntimeError("Token não encontrado no .env")

# ==========================
# UTIL
# ==========================

def validate_repo():
    try:
        subprocess.check_output(["git","rev-parse","--is-inside-work-tree"],cwd=REPO_DIR)
        return True
    except:
        return False

def log_execution(cmd, success, output):
    with open(LOG_FILE,"a") as f:
        f.write(f"""
==============================
TIME: {datetime.now()}
COMMAND: {cmd}
SUCCESS: {success}
OUTPUT:
{output}
""")

def create_workspace():
    WORKSPACES_DIR.mkdir(parents=True,exist_ok=True)
    ws = WORKSPACES_DIR / f"ws_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    subprocess.run(["git","clone",str(REPO_DIR),str(ws)],stdout=subprocess.PIPE)
    return ws

def execute(cmd,cwd):
    r = subprocess.run(cmd,shell=True,cwd=cwd,capture_output=True,text=True)
    return r.returncode==0, r.stdout+r.stderr

def create_snapshot():
    snap_dir = DEV_DIR / "snapshots"
    snap_dir.mkdir(exist_ok=True)
    commit = subprocess.check_output(["git","rev-parse","--short","HEAD"],cwd=REPO_DIR).decode().strip()
    snap = snap_dir / f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{commit}.txt"
    snap.write_text(f"Snapshot criado em {datetime.now()} base {commit}")

def update_patterns(cmd):

    # === STRATEGY INTEGRATION ===
    try:
        import json
        data = json.loads(STRATEGY_FILE.read_text())
        now = str(datetime.now())

        data["last_update"] = now
        data["evolution_last_update"] = now

        data.setdefault("change_history", []).append({
            "type": "commit",
            "command": cmd,
            "commit": commit_hash,
            "timestamp": now
        })

        STRATEGY_FILE.write_text(json.dumps(data, indent=2))
    except Exception as e:
        pass

    file = DEV_DIR / "patterns.json"
    data = {}
    if file.exists():
        data = json.loads(file.read_text())
    data[cmd] = data.get(cmd,0)+1
    file.write_text(json.dumps(data,indent=2))

# ==========================
# STRATEGY
# ==========================

async def strategy_status(update:Update,context:ContextTypes.DEFAULT_TYPE):
    data = json.loads(STRATEGY_FILE.read_text())

    objective = data["objective_active"]["title"]

    priorities = "\n".join(
        [f"- {p['id']} | {p['title']} (peso {p['weight']})"
         for p in data["priorities"]]
    )

    roadmap = "\n".join([f"- {r}" for r in data["roadmap"]])

    await update.message.reply_text(
        f"📌 OBJETIVO ATIVO:\n{objective}\n\n"
        f"🎯 PRIORIDADES:\n{priorities}\n\n"
        f"🗺 ROADMAP (9 passos):\n{roadmap}"
    )

# ==========================
# HANDLER
# ==========================

async def handle(update:Update,context:ContextTypes.DEFAULT_TYPE):
    global EXECUTING, PENDING_CMD

    if update.effective_user.id != AUTHORIZED_USER:
        return

    text = update.message.text.strip()
    mode = detect_mode(text)

    update_strategy_focus(mode)

    log_strategy_decision("mode_detected", f"Mensagem classificada como {mode}")



    if mode == "modo_planejamento":

        await update.message.reply_text("🧠 Entrando em modo PLANEJAMENTO automático.")

        return



    if mode == "modo_analise":

        await update.message.reply_text("🔎 Entrando em modo ANÁLISE automática.")

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
    # ==========================
    # SELF-MOD CHECK
    # ==========================
    if is_self_mod_command(cmd):
        await update.message.reply_text("🛠 Detectado comando de self-modificação.")
        ok, result = apply_self_mod(cmd)
        if ok:
            await update.message.reply_text(result)
        else:
            await update.message.reply_text("❌ Self-mod falhou. Rollback executado.")
            await update.message.reply_text(result)
        return
      # ==========================
    PENDING_CMD = None

    if EXECUTING:
        await update.message.reply_text("Execução já em andamento.")
        return

    EXECUTING = True

    if not validate_repo():
        await update.message.reply_text("Repo inválido.")
        EXECUTING = False
        return

    await update.message.reply_text("Criando workspace...")
    ws = create_workspace()

    await update.message.reply_text("Executando...")
    success, output = execute(cmd, ws)

    if not success:
        shutil.rmtree(ws,ignore_errors=True)
        log_execution(cmd,False,output)
        await update.message.reply_text(f"Falha:\n{output}")
        await update.message.reply_text("Workspace destruído.")
        EXECUTING = False
        return

    await update.message.reply_text("Criando snapshot de segurança...")
    create_snapshot()

    subprocess.run(["cp","-r",f"{ws}/.",str(REPO_DIR)])
    subprocess.run(["git","add","."],cwd=REPO_DIR)

    status = subprocess.run(["git","status","--porcelain"],cwd=REPO_DIR,capture_output=True,text=True)

    if status.stdout.strip()=="":
        shutil.rmtree(ws,ignore_errors=True)
        await update.message.reply_text("Nenhuma alteração.")
        await update.message.reply_text("Workspace destruído.")
        EXECUTING = False
        return

    commit_msg = f"auto(dev): {cmd}"
    subprocess.run(["git","commit","-m",commit_msg],cwd=REPO_DIR)

    commit_hash = subprocess.check_output(["git","rev-parse","--short","HEAD"],cwd=REPO_DIR).decode().strip()

    shutil.rmtree(ws,ignore_errors=True)

    log_execution(cmd,True,output)
    update_patterns(cmd)

    # === STRATEGY INTEGRATION ===
    try:
        import json
        data = json.loads(STRATEGY_FILE.read_text())
        now = str(datetime.now())

        data["last_update"] = now
        data["evolution_last_update"] = now

        data.setdefault("change_history", []).append({
            "type": "commit",
            "command": cmd,
            "commit": commit_hash,
            "timestamp": now
        })

        STRATEGY_FILE.write_text(json.dumps(data, indent=2))
    except Exception as e:
        pass


    await update.message.reply_text(f"Aplicado commit {commit_hash}")
    await update.message.reply_text("Workspace destruído.")

    EXECUTING = False

# ==========================
# MAIN
# ==========================

def main():
    token = load_token()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("strategy",strategy_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle))
    print("DEV BOT ONLINE - CLEAN STABLE CORE")
    app.run_polling()

if __name__=="__main__":
    main()

# ==========================
# STRATEGIC POST-COMMIT LOOP
# ==========================

import json

def strategic_post_commit(cmd, commit_hash):
    data = json.loads(STRATEGY_FILE.read_text())

    # Atualizar histórico de mudanças
    change_entry = {
        "timestamp": str(datetime.now()),
        "command": cmd,
        "commit": commit_hash
    }

    data.setdefault("change_history", []).append(change_entry)

    # Atualizar last_update
    data["last_update"] = str(datetime.now())

    STRATEGY_FILE.write_text(json.dumps(data, indent=2))


# ==========================
# PRIORITY INTEGRATION
# ==========================

def strategic_priority_gate(cmd):
    from prioritizer_engine import prioritize_tasks
    tasks = prioritize_tasks()

    if not tasks:
        return True

    top_task = tasks[0]["title"].lower()

    if top_task not in cmd.lower():
        return False

    return True

# SELF MOD TEST

# ==========================
# SELF-MOD INTEGRATION
# ==========================

from selfmod_engine import create_selfmod_branch, rollback
import selfmod_validator

def is_self_mod_command(cmd):
    return "/srv/dev/dev_bot.py" in cmd

def apply_self_mod(cmd):
    branch = create_selfmod_branch()

    # Executar modificação
    subprocess.run(cmd, shell=True, cwd="/")

    # Validar sintaxe
    ok, error = selfmod_validator.validate_python_file("/srv/dev/dev_bot.py")

    if not ok:
        rollback()
        return False, error

    # Commit na branch
    subprocess.run(["git", "add", "."], cwd="/srv/dev")
    subprocess.run(["git", "commit", "-m", f"selfmod: {cmd}"], cwd="/srv/dev")

    # Merge na main
    subprocess.run(["git", "checkout", "main"], cwd="/srv/dev")
    subprocess.run(["git", "merge", branch], cwd="/srv/dev")

    return True, "Self-mod aplicado com sucesso."

# SELF MOD OK 2
