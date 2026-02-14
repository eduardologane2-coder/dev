import subprocess

DEV_PATH = "/srv/dev"

def verify_clean_repo():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=DEV_PATH,
        capture_output=True,
        text=True
    )
    return result.stdout.strip() == ""
