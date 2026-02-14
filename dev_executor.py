import os
import subprocess
import hashlib
from datetime import datetime

REPO_PATH = "/srv/repo"

# comandos permitidos (nível 1)
ALLOWED_COMMANDS = {
    "mkdir",
    "touch",
    "ls",
    "pwd",
    "echo"
}

# padrões proibidos
FORBIDDEN_PATTERNS = [
    "&&", ";", "|", ">", "<",
    "sudo", "rm", "bash", "sh",
    "python", "git", "chmod",
    "chown", "mv", "cp"
]


def is_safe(command: str) -> bool:
    command = command.strip()

    # bloquear encadeamento
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in command:
            return False

    parts = command.split()

    if not parts:
        return False

    # permitir apenas um comando simples
    if parts[0] not in ALLOWED_COMMANDS:
        return False

    return True


def execute(command: str):
    if not is_safe(command):
        return False, "Comando bloqueado por política de segurança."

    try:
        result = subprocess.run(
            command,
            cwd=REPO_PATH,
            shell=True,
            capture_output=True,
            text=True
        )

        success = result.returncode == 0
        output = result.stdout + result.stderr

        log_execution(command, success, output)

        return success, output

    except Exception as e:
        return False, str(e)


def log_execution(command, success, output):
    log_path = "/srv/dev/dev_exec.log"

    content = f"""
==============================
TIME: {datetime.utcnow()}
COMMAND: {command}
SUCCESS: {success}
OUTPUT:
{output}
"""

    with open(log_path, "a") as f:
        f.write(content)

    # gerar hash do registro
    sha = hashlib.sha256(content.encode()).hexdigest()
    with open(log_path, "a") as f:
        f.write(f"HASH: {sha}\n")
