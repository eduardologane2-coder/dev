import subprocess
from joseph_contract import register_event

def sync_last_commit():
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd="/srv/repo"
        ).decode().strip()

        register_event("repo_commit", {
            "commit": commit
        })

    except Exception as e:
        register_event("repo_sync_error", {
            "error": str(e)
        })
