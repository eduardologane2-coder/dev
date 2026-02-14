import json
from llm_engine import ask_llm

def cognitive_decision(instruction: str):
    prompt = f"""
Você é o núcleo cognitivo do Dev.

Analise a instrução abaixo e responda SOMENTE em JSON válido no formato:

{{
  "decision": "PLAN | EXECUTE | REJECT",
  "reason": "motivo curto",
  "plan": [
    "passo 1",
    "passo 2"
  ]
}}

Instrução:
{instruction}
"""
    response = ask_llm(prompt)

    try:
        data = json.loads(response)
        return data
    except:
        return {
            "decision": "REJECT",
            "reason": "Resposta inválida da LLM",
            "plan": []
        }
