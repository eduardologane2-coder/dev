from intention_engine import classify_intention
from llm_engine import ask_llm

ALLOWED_STATES = {"EXECUTE", "PLAN", "REJECT", "CONFIRM", "BRIEFING"}

def _base_response():
    return {
        "state": None,
        "plan": None,
        "justification": None,
        "confidence": 0.0,
        "risk": "LOW",
        "metadata": {}
    }

def cognitive_decision(text: str):
    intent = classify_intention(text)
    response = _base_response()

    if intent == "SHELL_COMMAND":
        response.update({
            "state": "EXECUTE",
            "plan": [text],
            "justification": "Comando shell detectado.",
            "confidence": 0.95,
            "risk": "LOW"
        })
        return response

    if intent == "STRATEGIC_INTENT":
        prompt = f"""
Você é o núcleo estratégico do Dev.
Gere um plano técnico estruturado em lista JSON simples.
Texto: {text}
"""
        try:
            plan = ask_llm(prompt)
        except Exception as e:
            response.update({
                "state": "REJECT",
                "justification": f"Erro LLM: {e}",
                "confidence": 0.4,
                "risk": "MEDIUM"
            })
            return response

        response.update({
            "state": "PLAN",
            "plan": [plan] if isinstance(plan, str) else plan,
            "justification": "Intenção estratégica detectada.",
            "confidence": 0.85,
            "risk": "LOW"
        })
        return response

    if intent == "CONFIRMATION":
        response.update({
            "state": "CONFIRM",
            "justification": "Confirmação aguardada.",
            "confidence": 0.9,
            "risk": "LOW"
        })
        return response

    response.update({
        "state": "BRIEFING",
        "justification": "Preciso entender melhor seu objetivo.",
        "confidence": 0.7,
        "risk": "LOW"
    })
    return response
