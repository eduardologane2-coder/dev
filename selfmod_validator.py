from executor import run
from pathlib import Path

def validate_python_file(path: str):
    p = Path(path)

    if not p.exists():
        return False, "Arquivo não existe."

    success, output = run(f'python3 -m py_compile {path}')
    if not success:
        return False, output

    return True, "Arquivo válido."
