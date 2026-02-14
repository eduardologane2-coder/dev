import json

def parse_plan(raw_plan: str):
    try:
        data = json.loads(raw_plan)
        return data, None
    except Exception as e:
        return None, f"JSON inválido: {e}"

def validate_plan_structure(plan: dict):
    if not isinstance(plan, dict):
        return False, "Plano não é dict"

    if "steps" not in plan:
        return False, "Campo 'steps' ausente"

    if not isinstance(plan["steps"], list):
        return False, "'steps' deve ser lista"

    for step in plan["steps"]:
        if not isinstance(step, dict):
            return False, "Step não é dict"
        if "type" not in step or "content" not in step:
            return False, "Step inválido"

    return True, None
