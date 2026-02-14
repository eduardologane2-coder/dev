import subprocess

def run_integrity_checks():
    result = subprocess.run(
        ["python3", "-m", "py_compile", "dev_bot.py"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stderr
