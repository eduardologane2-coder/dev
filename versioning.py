from datetime import datetime
from safe_executor import run_safe as run

def commit_all(message: str):
    run("git add .")
    success, output = run(f'git commit -m "{message} {datetime.now()}"')
    return success, output
