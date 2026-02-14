from prioritizer_engine import prioritize_tasks

def test_prioritization_order():
    tasks = prioritize_tasks()
    assert isinstance(tasks, list)
