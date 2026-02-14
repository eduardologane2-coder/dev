import json

def render_human(decision: dict) -> str:
    state = decision.get("state")

    if state == "BRIEFING":
        return decision.get("message", "Preciso de mais contexto.")

    if state == "PLAN_READY":
        plan = decision.get("plan")

        # Se vier como dict estruturado
        if isinstance(plan, dict):
            try:
                return "🧠 Plano estruturado:\n\n" + json.dumps(plan, indent=2, ensure_ascii=False)
            except:
                return "🧠 Plano estruturado disponível."

        # Se vier como string
        if isinstance(plan, str):
            return "🧠 Plano estruturado:\n\n" + plan

        return "🧠 Plano estruturado disponível."

    if state == "EXECUTE":
        return "⚙️ Preparando execução técnica."

    return "Estado cognitivo não reconhecido."
