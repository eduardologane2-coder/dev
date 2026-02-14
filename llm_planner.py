from llm_engine import call_llm

def generate_plan(instruction):
    prompt = f"""
Você é o cérebro estratégico do Dev.
Analise a instrução abaixo e produza:

1. Interpretação estratégica
2. Subtarefas técnicas
3. Riscos envolvidos
4. Recomendações

Instrução:
{instruction}
"""
    return call_llm(prompt)
