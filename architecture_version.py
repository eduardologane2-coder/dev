from pathlib import Path
from datetime import datetime

VERSION_FILE = Path("/srv/dev/.selfmod/architecture_version.txt")

def bump_version():
    VERSION_FILE.parent.mkdir(exist_ok=True)
    if not VERSION_FILE.exists():
        VERSION_FILE.write_text("1\n")
        return 1
    v = int(VERSION_FILE.read_text().strip()) + 1
    VERSION_FILE.write_text(str(v) + "\n")
    return v
