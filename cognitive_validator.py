ALLOWED_STATES = {"EXECUTE", "PLAN", "REJECT", "CONFIRM", "BRIEFING"}

def validate_cognitive_contract(data: dict):
    if not isinstance(data, dict):
        return False, "Resposta não é dict"

    required_fields = {"state", "confidence", "risk", "metadata"}
    if not required_fields.issubset(data.keys()):
        return False, "Campos obrigatórios ausentes"

    if data["state"] not in ALLOWED_STATES:
        return False, "State inválido"

    if not isinstance(data["confidence"], (int, float)):
        return False, "Confidence inválido"

    if data["risk"] not in {"LOW", "MEDIUM", "HIGH"}:
        return False, "Risk inválido"

    if data["state"] == "PLAN" and not data.get("plan"):
        return False, "PLAN sem plano"

    return True, "OK"
