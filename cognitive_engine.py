import json
from pathlib import Path
from datetime import datetime
from llm_engine import ask_llm

COGNITIVE_LOG = Path("/srv/dev/cognitive_log.json")

def _ensure_log():
    if not COGNITIVE_LOG.exists():
        COGNITIVE_LOG.write_text(json.dumps([], indent=2))

def _log(entry):
    _ensure_log()
    data = json.loads(COGNITIVE_LOG.read_text())
    data.append(entry)
    COGNITIVE_LOG.write_text(json.dumps(data, indent=2))

def cognitive_decision(instruction: str):
    prompt = f"""
Você é o núcleo cognitivo do Dev.

Classifique a instrução abaixo.

Instrução:
{instruction}

Responda obrigatoriamente em JSON válido no formato:

{{
  "state": "ANALYZE | PLAN | EXECUTE | REJECT",
  "justification": "explicação curta"
}}
"""

    response = ask_llm(prompt)

    try:
        parsed = json.loads(response)
    except:
        parsed = {
            "state": "ANALYZE",
            "justification": "Falha no parse. Default ANALYZE."
        }

    entry = {
        "timestamp": str(datetime.now()),
        "instruction": instruction,
        "decision": parsed["state"],
        "justification": parsed["justification"]
    }

    _log(entry)

    return parsed["state"], parsed["justification"]
