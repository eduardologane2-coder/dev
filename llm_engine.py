import os
import requests

def load_llm_key():
    with open("/srv/dev/.env") as f:
        for line in f:
            if line.startswith("LLM_API_KEY="):
                return line.split("=",1)[1].strip().replace('"','')
    return None

LLM_API_KEY = load_llm_key()

def call_llm(prompt):
    if not LLM_API_KEY:
        return "LLM_API_KEY não configurada."

    # Exemplo usando OpenAI API compatível
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Você é o motor cognitivo estratégico do Dev."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4
        }
    )

    if response.status_code != 200:
        return f"Erro LLM: {response.text}"

    data = response.json()
    return data["choices"][0]["message"]["content"]
