from metacognition_engine import recalculate_meta, get_meta
from semantic_memory_engine import register_pattern

register_pattern("teste meta", "EXECUTE", 0.9)
register_pattern("teste meta2", "PLAN_READY", 0.8)

recalculate_meta()
meta = get_meta()

assert meta["samples"] >= 2
assert meta["avg_confidence"] > 0

print("OK")
