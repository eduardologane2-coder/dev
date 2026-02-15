from pathlib import Path

BASE_PATH = Path("/srv/dev").resolve()
SANDBOX_PATH = (BASE_PATH / "sandbox").resolve()
WORKSPACE_PATH = (BASE_PATH / "workspaces").resolve()
KERNEL_PATH = (BASE_PATH / "core_kernel").resolve()

def is_protected(path: Path) -> bool:
    path = path.resolve()

    # Protege apenas o núcleo real
    if KERNEL_PATH in path.parents or path == KERNEL_PATH:
        return True

    # Protege executor principal
    if path.name in ["executor.py", "dev_bot.py"]:
        return True

    return False


def is_inside_sandbox(path: Path) -> bool:
    path = path.resolve()

    return (
        SANDBOX_PATH in path.parents or
        path == SANDBOX_PATH or
        WORKSPACE_PATH in path.parents
    )
