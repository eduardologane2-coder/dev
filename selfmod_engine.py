import subprocess
from datetime import datetime
from metrics_engine import inc

DEV_PATH = "/srv/dev"

def create_selfmod_branch():
    branch = "selfmod_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    subprocess.run(["git", "checkout", "-b", branch], cwd=DEV_PATH)
    return branch

def commit_selfmod(message):
    subprocess.run(["git", "add", "."], cwd=DEV_PATH)
    subprocess.run(["git", "commit", "-m", message], cwd=DEV_PATH)
    subprocess.run(["git", "checkout", "main"], cwd=DEV_PATH)
    subprocess.run(["git", "merge", "--ff-only", "HEAD@{1}"], cwd=DEV_PATH)
    inc("selfmods")
    inc("commits")

def rollback():
    subprocess.run(["git", "reset", "--hard"], cwd=DEV_PATH)
    subprocess.run(["git", "checkout", "main"], cwd=DEV_PATH)
    inc("rollbacks")
