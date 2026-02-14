import subprocess
from datetime import datetime
from pathlib import Path

from selfmod_validator import validate_python_file
from selfmod_policy import ALLOWED_FILES, PROTECTED_FILES
from metrics_engine import inc

DEV_PATH = Path("/srv/dev")

# ==========================
# DETECÇÃO
# ==========================

def is_self_mod_command(cmd: str) -> bool:
    return "/srv/dev/" in cmd

# ==========================
# APLICAÇÃO
# ==========================

def apply_self_mod(cmd: str):
    try:
        # Detectar arquivo alvo
        parts = cmd.split(">>")
        if len(parts) != 2:
            return False, "Formato inválido para self-mod."

        target_path = parts[1].strip()
        target_file = Path(target_path).name

        if target_file in PROTECTED_FILES:
            return False, "Arquivo protegido por política."

        if target_file not in ALLOWED_FILES:
            return False, "Arquivo não permitido para self-mod."

        branch = "selfmod_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        subprocess.run(["git","checkout","-b",branch],cwd=DEV_PATH,check=True)

        subprocess.run(cmd,shell=True,cwd="/",check=True)

        ok,error = validate_python_file(Path(target_path))
        if not ok:
            subprocess.run(["git","reset","--hard"],cwd=DEV_PATH)
            subprocess.run(["git","checkout","main"],cwd=DEV_PATH)
            inc("rollbacks")
            return False, error

        subprocess.run(["git","add",target_path],cwd=DEV_PATH,check=True)
        subprocess.run(["git","commit","-m",f"selfmod: {cmd}"],cwd=DEV_PATH,check=True)
        subprocess.run(["git","checkout","main"],cwd=DEV_PATH,check=True)
        subprocess.run(["git","merge",branch],cwd=DEV_PATH,check=True)

        inc("selfmods")
        return True, "Self-mod aplicado com sucesso."

    except Exception as e:
        subprocess.run(["git","reset","--hard"],cwd=DEV_PATH)
        subprocess.run(["git","checkout","main"],cwd=DEV_PATH)
        inc("rollbacks")
        return False, str(e)
