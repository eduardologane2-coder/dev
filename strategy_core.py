import json
from pathlib import Path
from datetime import datetime

DEV_DIR = Path("/srv/dev")
STRATEGY_FILE = DEV_DIR / "strategy.json"

def load_strategy():
    return json.loads(STRATEGY_FILE.read_text())

def save_strategy(data):
    data["last_update"] = str(datetime.now())
    STRATEGY_FILE.write_text(json.dumps(data, indent=2))

def update_mode(mode):
    data = load_strategy()
    data["current_mode"] = mode
    save_strategy(data)

def register_change(change_type, payload):
    data = load_strategy()
    data.setdefault("change_history", []).append({
        "type": change_type,
        "payload": payload,
        "timestamp": str(datetime.now())
    })
    save_strategy(data)
