CONFIDENCE_THRESHOLD = 0.85

def allow_execution(decision: dict) -> bool:
    state = decision.get("state")
    confidence = decision.get("confidence", 0)

    if state != "EXECUTE":
        return False

    return confidence >= CONFIDENCE_THRESHOLD
