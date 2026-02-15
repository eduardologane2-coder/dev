from datetime import datetime
from safe_executor import run_safe as run

def auto_commit(tag="auto"):
    run("git add .")
    success, output = run(f'git commit -m "{tag} {datetime.now()}"')
    return success, output
