import json
from pathlib import Path
from llm_engine import ask_llm

STRATEGY_FILE = Path("/srv/dev/strategy.json")

def evaluate_strategy(instruction: str):
    data = json.loads(STRATEGY_FILE.read_text())
    objective = data["objective_active"]["title"]

    prompt = f"""
Você é o núcleo estratégico do Dev.

Objetivo ativo:
{objective}

Nova instrução:
{instruction}

Responda apenas com uma das opções:
- EXECUTE
- PLAN
- REJECT

E explique brevemente o motivo.
"""

    response = ask_llm(prompt)

    decision = "EXECUTE"
    if "PLAN" in response.upper():
        decision = "PLAN"
    elif "REJECT" in response.upper():
        decision = "REJECT"

    return decision, response
