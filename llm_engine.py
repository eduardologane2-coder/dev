import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega .env explicitamente
load_dotenv("/srv/dev/.env")

def ask_llm(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER")
    model = os.getenv("LLM_MODEL")
    api_key = os.getenv("LLM_API_KEY")

    if not api_key:
        return "LLM não configurada no .env (LLM_API_KEY ausente)"

    if provider != "openai":
        return f"Provider não suportado: {provider}"

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é o núcleo cognitivo estratégico do Dev."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Erro LLM: {e}"
