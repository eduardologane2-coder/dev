def validate_decision(data: dict):
    required = ["state", "confidence"]
    for r in required:
        if r not in data:
            return False, f"Campo ausente: {r}"

    if not (0 <= data["confidence"] <= 1):
        return False, "Confidence inválida"

    return True, "OK"
