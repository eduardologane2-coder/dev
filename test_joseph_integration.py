import json
from joseph_contract import register_event, load_joseph_state

def test_register_event():
    register_event("test_event", {"ok": True})
    data = load_joseph_state()
    assert data["events"][-1]["type"] == "test_event"
