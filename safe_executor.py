import subprocess
from pathlib import Path
from core_kernel.kernel_guard import WORKSPACE_PATH

def safe_execute(command: str, workspace: Path):
    if WORKSPACE_PATH not in workspace.parents:
        return False, "⛔ Execução permitida apenas dentro de workspace isolada."
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(workspace),
            capture_output=True,
            text=True,
            timeout=10
        )
        return True, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)
