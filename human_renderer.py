def render_human(decision):
    state = decision.get("state")

    if state == "PLAN_READY":
        return "🧠 Plano estruturado:\n\n" + decision.get("plan")

    if state == "BRIEFING":
        return decision.get("message")

    if state == "EXECUTE":
        return "⚙️ Comando técnico identificado."

    return "Estado cognitivo desconhecido."
