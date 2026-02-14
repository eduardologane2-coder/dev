import subprocess
from pathlib import Path

REPO_DIR = Path("/srv/repo")

# ==========================
# VALIDAÇÃO DE PLANO
# ==========================

def validate_plan(plan_steps):
    if not isinstance(plan_steps, list):
        return False, "Plano não é lista."

    for step in plan_steps:
        if not isinstance(step, dict):
            return False, "Step inválido."
        if "command" not in step:
            return False, "Step sem comando."

    return True, "OK"

# ==========================
# EXECUÇÃO DE PLANO
# ==========================

def execute_plan(plan_steps):
    results = []

    for step in plan_steps:
        cmd = step.get("command")

        result = subprocess.run(
            cmd,
            shell=True,
            cwd=REPO_DIR,
            capture_output=True,
            text=True
        )

        results.append({
            "command": cmd,
            "success": result.returncode == 0,
            "output": result.stdout + result.stderr
        })

        if result.returncode != 0:
            break

    return results
