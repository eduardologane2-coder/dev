import subprocess
from datetime import datetime
from pathlib import Path
from selfmod_validator import validate_python_file
from selfmod_policy import is_allowed_selfmod

DEV_PATH = "/srv/dev"

def create_selfmod_branch():
    branch = "selfmod_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    subprocess.run(["git", "checkout", "-b", branch], cwd=DEV_PATH, check=True)
    return branch

def rollback():
    subprocess.run(["git", "reset", "--hard"], cwd=DEV_PATH)
    subprocess.run(["git", "checkout", "main"], cwd=DEV_PATH)

def extract_target(cmd: str):
    if ">>" not in cmd:
        return None
    return cmd.split(">>")[-1].strip()

def execute_selfmod(cmd: str):
    target = extract_target(cmd)
    if not target:
        raise RuntimeError("Target file not detected.")

    name = Path(target).name

    if not is_allowed_selfmod(name):
        raise RuntimeError("Arquivo protegido ou não permitido.")

    branch = create_selfmod_branch()

    subprocess.run(cmd, shell=True, cwd=DEV_PATH, check=True)

    subprocess.run(["git", "add", name], cwd=DEV_PATH, check=True)
    subprocess.run(["git", "commit", "-m", f"selfmod: {cmd}"], cwd=DEV_PATH, check=True)

    ok, error = validate_python_file(Path(DEV_PATH) / name)
    if not ok:
        rollback()
        raise RuntimeError(error)

    subprocess.run(["git", "checkout", "main"], cwd=DEV_PATH, check=True)
    subprocess.run(["git", "merge", branch], cwd=DEV_PATH, check=True)

    return branch
