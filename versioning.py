import subprocess
from datetime import datetime


class Versioning:

    def commit(self, description: str):
        timestamp = datetime.utcnow().isoformat()

        message = f"[DEV AUTO COMMIT]\n\n{description}\n\nTimestamp: {timestamp}"

        subprocess.run("git add .", shell=True)
        subprocess.run(f'git commit -m "{message}"', shell=True)
