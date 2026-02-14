def classify_intention(text: str) -> str:
    lower = text.strip().lower()

    if lower in ["sim", "não", "nao"]:
        return "CONFIRMATION"

    if any(word in lower for word in ["mkdir", "touch", "echo", "rm ", "git ", "cd "]):
        return "SHELL_COMMAND"

    if any(word in lower for word in ["melhorar", "arquitetura", "estratégia", "planejar", "analisar"]):
        return "STRATEGIC_INTENT"

    return "UNKNOWN"
