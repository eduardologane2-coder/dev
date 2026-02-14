import subprocess
from datetime import datetime

REPO_PATH = "/srv/repo"

def run(cmd):
    return subprocess.run(
        cmd,
        cwd=REPO_PATH,
        shell=True,
        capture_output=True,
        text=True
    )

def commit_if_needed(command_executed: str):
    # adiciona alterações
    run("git add .")

    # verifica se há mudanças staged
    diff_check = run("git diff --cached --quiet")

    if diff_check.returncode == 0:
        return False, "Nenhuma alteração para commit."

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"auto: {command_executed} | {timestamp}"

    commit = run(f'git commit -m "{message}"')

    if commit.returncode != 0:
        return False, commit.stderr

    return True, message
