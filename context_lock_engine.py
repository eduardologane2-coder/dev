import json
from pathlib import Path
from llm_engine import ask_llm

STATE_FILE = Path("/srv/dev/context_lock.json")

EXECUTION_THRESHOLD = 3
HARD_ABORT_THRESHOLD = 5

def load_state():
    if not STATE_FILE.exists():
        return {"active": False, "topic": None, "confidence_level": 0}
    return json.loads(STATE_FILE.read_text())

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def activate(topic: str):
    state = {
        "active": True,
        "topic": topic,
        "confidence_level": 1
    }
    save_state(state)

def escalate_confidence():
    state = load_state()
    if state["active"]:
        state["confidence_level"] += 1
        save_state(state)

def deactivate():
    save_state({"active": False, "topic": None, "confidence_level": 0})

def can_auto_execute():
    state = load_state()
    return state["confidence_level"] >= EXECUTION_THRESHOLD

def requires_hard_confirmation():
    state = load_state()
    return state["confidence_level"] >= HARD_ABORT_THRESHOLD

def interpret_abort_response(user_text: str):
    lower = user_text.lower()

    if any(x in lower for x in ["sim", "executar", "pode executar"]):
        return "ABORT_AND_EXECUTE"

    if any(x in lower for x in ["não", "continuar"]):
        return "CONTINUE_BRIEFING"

    if any(x in lower for x in ["converter", "parte do plano"]):
        return "CONVERT_TO_PLAN"

    prompt = f"""
Estamos em um briefing estratégico ativo.
Usuário respondeu: "{user_text}"

Classifique apenas como:
- ABORT_AND_EXECUTE
- CONTINUE_BRIEFING
- CONVERT_TO_PLAN
"""
    try:
        resp = ask_llm(prompt)
        resp = resp.strip().upper()
        if resp in ["ABORT_AND_EXECUTE","CONTINUE_BRIEFING","CONVERT_TO_PLAN"]:
            return resp
    except:
        pass

    return "AMBIGUOUS"
