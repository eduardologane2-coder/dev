from architecture_audit import run_integrity_checks
from architecture_state import load_state

def test_integrity():
    ok, _ = run_integrity_checks()
    assert ok

def test_state_load():
    state = load_state()
    assert "stability_score" in state
