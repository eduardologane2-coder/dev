import json
from evolution_transition_engine import evaluate_stage

def test_stage_transition():
    metrics = {"commits": 25, "executions": 15, "selfmods": 6, "rollbacks": 2}
    stage = evaluate_stage(metrics)
    assert stage == "strategic"
