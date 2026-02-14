from datetime import datetime
from pathlib import Path
from selfmod_validator import validate_python_file
from selfmod_policy import ALLOWED_FILES, PROTECTED_FILES
from metrics_engine import inc

DEV_PATH = Path("/srv/dev")

def is_self_mod_command(cmd: str) -> bool:
    return "/srv/dev/" in cmd

def build_self_mod_request(cmd: str):
    """
    NÃO executa nada.
    Apenas valida e retorna requisição estruturada.
    """

    parts = cmd.split(">>")
    if len(parts) != 2:
        return False, "Formato inválido para self-mod."

    target_path = parts[1].strip()
    target_file = Path(target_path).name

    if target_file in PROTECTED_FILES:
        return False, "Arquivo protegido por política."

    if target_file not in ALLOWED_FILES:
        return False, "Arquivo não permitido para self-mod."

    valid, message = validate_python_file(target_path)
    if not valid:
        return False, message

    return True, {
        "type": "EXECUTION_REQUEST",
        "origin": "selfmod_engine",
        "risk": "medium",
        "commands": [
            cmd,
            f'git add {target_path}',
            f'git commit -m "selfmod: {target_file} {datetime.now()}"'
        ]
    }
