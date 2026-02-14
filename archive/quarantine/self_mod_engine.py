#!/usr/bin/env python3
import subprocess
from datetime import datetime
from pathlib import Path

DEV_DIR = Path("/srv/dev")
REPO_DIR = Path("/srv/repo")
SELF_FILE = DEV_DIR / "dev_bot.py"

def is_self_modification(cmd: str) -> bool:
    return "dev_bot.py" in cmd or str(SELF_FILE) in cmd

def create_branch():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch = f"feature/self_mod_{ts}"
    subprocess.run(["git", "checkout", "-b", branch], cwd=REPO_DIR)
    return branch

def validate_syntax():
    result = subprocess.run(
        ["python3", "-m", "py_compile", str(SELF_FILE)],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stderr

def run_tests():
    test_dir = DEV_DIR / "tests"
    if not test_dir.exists():
        return True, "Sem testes definidos"
    result = subprocess.run(
        ["python3", "-m", "pytest", str(test_dir)],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout + result.stderr

def rollback():
    subprocess.run(["git", "reset", "--hard"], cwd=REPO_DIR)
    subprocess.run(["git", "checkout", "main"], cwd=REPO_DIR)
