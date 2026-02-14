from intention_engine import classify_intention
from llm_engine import ask_llm
import json

CONFIDENCE_THRESHOLD = 0.85

def cognitive_decision(text: str):
    intent = classify_intention(text)

    # EXECUÇÃO DIRETA
    if intent == "SHELL_COMMAND":
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
            return {
                "state": "BRIEFING",
                "message": "Plano inválido. Necessário mais contexto.",
                "confidence": 0.4
            }

        return {
            "state": "PLAN_READY",
            "plan": plan,
            "confidence": 0.8
        }

    if intent == "CONFIRMATION":
        return {
            "state": "CONFIRM",
            "confidence": 0.7
        }

    return {
        "state": "BRIEFING",
        "message": "Preciso entender melhor seu objetivo.",
        "confidence": 0.6
    }
