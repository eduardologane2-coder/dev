from safe_executor import run_safe as run
from pathlib import Path

DEV_PATH = Path("/srv/dev")

def audit_git_state():
    success, output = run("git status", cwd=DEV_PATH)

    if not success:
        return False, output

    return True, output
