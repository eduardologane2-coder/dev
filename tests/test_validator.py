import subprocess

def test_validator():
    result = subprocess.run(
        ["python3", "selfmod_validator.py", "dev_bot.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
