from phase_engine import evaluate_phase, get_phase
from semantic_memory_engine import register_pattern
from metacognition_engine import recalculate_meta

# simular decisões estratégicas
for i in range(40):
    register_pattern("teste", "PLAN_READY", 0.9)

recalculate_meta()
phase = evaluate_phase()

assert phase in ["STRATEGIC", "ARCHITECTURAL", "AUTONOMOUS"]

print("OK")
