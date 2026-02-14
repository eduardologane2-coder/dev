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

def run_command(cmd: str, cwd: Path = None):
    if not is_safe(cmd):
        return False, "Comando bloqueado por política de segurança."

    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd or WORKSPACE,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return False, result.stderr.strip()

    return True, result.stdout.strip()

def execute_request(request: dict):
    if request.get("type") != "EXECUTION_REQUEST":
        return False, "Tipo inválido."

    results = []

    for cmd in request.get("commands", []):
        success, output = run_command(cmd)
        results.append({
            "command": cmd,
            "success": success,
            "output": output
        })

        if not success:
            break

    return True, results
