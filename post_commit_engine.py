import json
from datetime import datetime
from pathlib import Path

DEV_DIR = Path("/srv/dev")
STRATEGY_FILE = DEV_DIR / "strategy.json"

def strategic_post_commit_update(commit_hash, command):
    """
    Atualiza roadmap e histórico estratégico após commit.
    """
    data = json.loads(STRATEGY_FILE.read_text())

    data["change_history"].append({
        "timestamp": str(datetime.now()),
        "commit": commit_hash,
        "command": command
    })

    data["last_update"] = str(datetime.now())

    STRATEGY_FILE.write_text(json.dumps(data, indent=2))
