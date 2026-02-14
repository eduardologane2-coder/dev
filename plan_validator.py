def validate_plan(plan_steps):
    if not plan_steps:
        return False, "Plano vazio"

    if len(plan_steps) > 20:
        return False, "Plano excessivamente grande"

    return True, "Plano válido"
