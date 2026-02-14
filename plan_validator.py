def validate_plan(plan):
    if not plan:
        return False, "Plano vazio."

    if isinstance(plan, str):
        return True, "Plano textual aceito."

    if isinstance(plan, list):
        if len(plan) == 0:
            return False, "Plano sem passos."
        return True, "Plano válido."

    return False, "Formato de plano inválido."
