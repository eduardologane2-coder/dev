from semantic_memory_engine import register_pattern, get_recent_patterns

register_pattern("teste arquitetura", "PLAN_READY", 0.8)
patterns = get_recent_patterns()

assert len(patterns) >= 1
assert "topic" in patterns[-1]

print("OK")
