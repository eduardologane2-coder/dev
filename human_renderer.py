def render_human(decision: dict) -> str:
    state = decision.get("state")
    confidence = decision.get("confidence", 0)

    if state == "BRIEFING":
        return decision.get("message")

    if state == "PLAN_READY":
        return "🧠 Plano estruturado:\n\n" + decision.get("plan")

    if state == "EXECUTE":
        return "⚙️ Comando técnico detectado."

    if state == "REJECT":
        return "🚫 Instrução rejeitada."

    return "Estado cognitivo inválido."
