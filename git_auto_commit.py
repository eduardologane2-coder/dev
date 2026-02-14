from datetime import datetime
from executor import run

def auto_commit(tag="auto"):
    run("git add .")
    success, output = run(f'git commit -m "{tag} {datetime.now()}"')
    return success, output
