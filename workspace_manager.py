from pathlib import Path
from datetime import datetime
from core_kernel.kernel_guard import is_protected, is_inside_sandbox, SANDBOX_PATH, WORKSPACE_PATH

def create_workspace():
    WORKSPACE_PATH.mkdir(exist_ok=True)
    ws_name = "ws_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    ws_path = WORKSPACE_PATH / ws_name
    ws_path.mkdir()
    return ws_path

def safe_write(path: Path, content: str):
    if is_protected(path):
        return False, "⛔ Núcleo protegido."
    if not is_inside_sandbox(path):
        return False, "⛔ Escrita permitida apenas dentro da sandbox."
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True, "✅ Arquivo escrito com segurança."
