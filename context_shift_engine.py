from cognitive_score_engine import decrease

def detect_shift(current_topic: str, new_text: str):
    if current_topic and current_topic.lower() not in new_text.lower():
        decrease(2)
        return True
    return False
