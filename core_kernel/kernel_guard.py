from pathlib import Path

BASE_PATH = Path("/srv/dev").resolve()
SANDBOX_PATH = BASE_PATH / "sandbox"
WORKSPACE_PATH = BASE_PATH / "workspaces"
KERNEL_PATH = BASE_PATH / "core_kernel"

PROTECTED_PATHS = [
    BASE_PATH,
    KERNEL_PATH
]

def is_protected(path: Path) -> bool:
    path = path.resolve()
    for protected in PROTECTED_PATHS:
        if path == protected or protected in path.parents:
            return True
    return False

def is_inside_sandbox(path: Path) -> bool:
    path = path.resolve()
    return SANDBOX_PATH in path.parents or path == SANDBOX_PATH
