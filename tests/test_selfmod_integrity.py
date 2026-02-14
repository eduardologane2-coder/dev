import subprocess

def test_integrity():
    result = subprocess.run(
        ["python3", "selfmod_integrity.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
