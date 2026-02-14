import subprocess
from pathlib import Path

def validate_python_file(path: Path):
    result = subprocess.run(
        ["python3", "-m", "py_compile", str(path)],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stderr
