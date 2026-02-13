import subprocess
import sys
from pathlib import Path

def validate_python_file(path):
    result = subprocess.run(
        ["python3", "-m", "py_compile", str(path)],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stderr

if __name__ == "__main__":
    file = Path(sys.argv[1])
    ok, error = validate_python_file(file)
    if ok:
        print("VALID")
        sys.exit(0)
    else:
        print(error)
        sys.exit(1)
