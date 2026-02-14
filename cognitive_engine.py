from intention_engine import classify_intention
from llm_engine import ask_llm
import json

def cognitive_decision(text: str):
    intent = classify_intention(text)

    if intent == "SHELL_COMMAND":
        return {
            "state": "EXECUTE",
            "plan": [text],
            "confidence": 0.95
        }

    if intent == "STRATEGIC_INTENT":
        prompt = f"""
Você é o núcleo estratégico do Dev.

Responda SOMENTE em JSON válido com o formato:

{{
  "state": "BRIEFING" ou "PLAN_READY",
  "plan": "texto ou null",
  "message": "texto ou null",
  "confidence": 0.0-1.0
}}

Se faltar contexto → BRIEFING.
Se estiver claro → PLAN_READY com plano numerado.

Texto: {text}
"""

        raw = ask_llm(prompt)

        try:
            data = json.loads(raw)
            return data
        except:
            return {
                "state": "BRIEFING",
                "message": "Preciso de mais contexto.",
                "confidence": 0.4
            }

    if intent == "CONFIRMATION":
        return {
            "state": "CONFIRM",
            "confidence": 0.7
        }

    return {
        "state": "BRIEFING",
        "message": "Explique melhor seu objetivo.",
        "confidence": 0.5
    }
