import json
from pathlib import Path
from semantic_memory_engine import get_recent_patterns

META_FILE = Path("/srv/dev/metacognition.json")

def _load():
    if not META_FILE.exists():
        return {
            "avg_confidence": 0.0,
            "execute_ratio": 0.0,
            "plan_ratio": 0.0,
            "samples": 0
        }
    return json.loads(META_FILE.read_text())

def _save(data):
    META_FILE.write_text(json.dumps(data, indent=2))

def recalculate_meta():
    patterns = get_recent_patterns(limit=50)

    if not patterns:
        return _load()

    total = len(patterns)
    avg_conf = sum(p["confidence"] for p in patterns) / total

    execute_count = sum(1 for p in patterns if p["state"] == "EXECUTE")
    plan_count = sum(1 for p in patterns if p["state"] == "PLAN_READY")

    data = {
        "avg_confidence": round(avg_conf, 3),
        "execute_ratio": round(execute_count / total, 3),
        "plan_ratio": round(plan_count / total, 3),
        "samples": total
    }

    _save(data)
    return data

def get_meta():
    return _load()
