from executor import run
from pathlib import Path

DEV_PATH = Path("/srv/dev")

def check_git_clean():
    success, output = run("git status --porcelain", cwd=DEV_PATH)

    if not success:
        return False, output

    if output.strip() != "":
        return False, "Repositório possui alterações pendentes."

    return True, "Repositório íntegro."
