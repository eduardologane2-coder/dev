from intention_engine import classify_intention
from llm_engine import ask_llm
import json

CONFIDENCE_THRESHOLD = 0.85

def cognitive_decision(text: str):
    from semantic_memory_engine import register_pattern
    from metacognition_engine import recalculate_meta
    recalculate_meta()
    intent = classify_intention(text)

    # EXECUÇÃO DIRETA
    if intent == "SHELL_COMMAND":
        register_pattern(text, "EXECUTE", 0.9)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
        register_pattern(text, "PLAN_READY", 0.8)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
        return {
            "state": "EXECUTE",
            "plan": {
                "steps": [
                    {"type": "shell", "content": text}
                ]
            },
            "confidence": 0.95
        }

    # INTENÇÃO ESTRATÉGICA
    if intent == "STRATEGIC_INTENT":
        prompt = f"""
Responda SOMENTE em JSON válido.

Formato obrigatório:
{{
  "steps": [
    {{
      "type": "analysis|shell|refactor|question",
      "content": "descrição objetiva"
    }}
  ]
}}

Se faltar contexto, gere apenas um step do tipo "question".

Texto: {text}
"""

        raw = ask_llm(prompt)

        try:
            plan = json.loads(raw)
        except:
        register_pattern(text, "EXECUTE", 0.9)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
        register_pattern(text, "PLAN_READY", 0.8)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
            return {
                "state": "BRIEFING",
                "message": "Plano inválido. Necessário mais contexto.",
                "confidence": 0.4
            }

        register_pattern(text, "EXECUTE", 0.9)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
        register_pattern(text, "PLAN_READY", 0.8)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
        return {
            "state": "PLAN_READY",
            "plan": plan,
            "confidence": 0.8
        }

    if intent == "CONFIRMATION":
        register_pattern(text, "EXECUTE", 0.9)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
        register_pattern(text, "PLAN_READY", 0.8)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
        return {
            "state": "CONFIRM",
            "confidence": 0.7
        }

        register_pattern(text, "EXECUTE", 0.9)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
        register_pattern(text, "PLAN_READY", 0.8)
    from metacognition_engine import recalculate_meta
    recalculate_meta()
    return {
        "state": "BRIEFING",
        "message": "Preciso entender melhor seu objetivo.",
        "confidence": 0.6
    }
