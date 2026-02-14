from conflict_engine import detect_conflict

def test_conflict_detection():
    conflict, _ = detect_conflict("Apagar estratégia atual")
    assert conflict is True
