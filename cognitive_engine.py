from intention_engine import classify_intention
from llm_engine import ask_llm

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
Se houver contexto suficiente, gere plano técnico estruturado numerado.
Caso contrário, peça apenas as informações faltantes.
Texto: {text}
"""
        response = ask_llm(prompt)

        if not response or len(response.strip()) < 20:
            return {
                "state": "BRIEFING",
                "message": "Preciso de mais contexto antes de estruturar um plano.",
                "confidence": 0.5
            }

        return {
            "state": "PLAN_READY",
            "plan": response.strip(),
            "confidence": 0.8
        }

    return {
        "state": "BRIEFING",
        "message": "Preciso entender melhor seu objetivo.",
        "confidence": 0.4
    }
