from evolution_engine import run_integrity_checks

def test_integrity():
    ok, _ = run_integrity_checks()
    assert ok
