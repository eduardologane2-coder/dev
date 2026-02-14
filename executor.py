import subprocess
from pathlib import Path

WORKSPACE = Path("/srv/dev/workspace").resolve()

FORBIDDEN = [
    "rm -rf /",
    "rm -rf /*",
    "shutdown",
    "reboot",
]

def is_safe(cmd: str):
    for f in FORBIDDEN:
        if f in cmd:
            return False
    return True

def execute(cmd: str):
    if not is_safe(cmd):
        return False, "Comando bloqueado por política de segurança."

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=WORKSPACE,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return False, result.stderr.strip()

        return True, result.stdout.strip()

    except Exception as e:
        return False, str(e)
