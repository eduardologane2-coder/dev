from pathlib import Path

ALLOWED_FILES = {
    "dev_bot.py",
    "prioritizer_engine.py",
    "conflict_engine.py",
    "evolution_engine.py"
}

PROTECTED_FILES = {
    "selfmod_engine.py",
    "selfmod_validator.py",
    "selfmod_policy.py",
    "selfmod_integrity.py"
}

def is_allowed_selfmod(target_file: str) -> bool:
    name = Path(target_file).name
    if name in PROTECTED_FILES:
        return False
    return name in ALLOWED_FILES
