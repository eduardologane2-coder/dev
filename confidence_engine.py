AUTO_EXEC_THRESHOLD = 0.9

def can_auto_execute(decision):
    return decision.get("confidence", 0) >= AUTO_EXEC_THRESHOLD
