import subprocess
from pathlib import Path

REPO_DIR = Path("/srv/repo")

def analyze_workspace_impact(workspace_path):
    """
    Analisa arquivos modificados antes de aplicar no repositório.
    """
    subprocess.run(["git", "add", "."], cwd=workspace_path)

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=workspace_path,
        capture_output=True,
        text=True
    )

    changes = result.stdout.strip().splitlines()

    risk_level = "low"

    for line in changes:
        if ".py" in line:
            risk_level = "medium"
        if "dev_bot.py" in line:
            risk_level = "high"

    return {
        "files_changed": changes,
        "risk": risk_level
    }
