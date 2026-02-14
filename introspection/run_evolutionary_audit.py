import json
from introspection.self_inspection_engine import SelfInspectionEngine
from llm_engine import ask_llm

def build_prompt(structural_report: dict) -> str:
    return f"""
Você está auditando sua própria arquitetura interna.

TAREFA:

1. Identifique riscos arquiteturais reais.
2. Identifique acoplamentos perigosos.
3. Identifique múltiplos pontos de execução.
4. Identifique duplicidades conceituais.
5. Identifique ausência de separação clara de camadas.
6. Avalie maturidade arquitetural (0-10).
7. Sugira evolução estrutural mínima (não revolução).
8. Não proponha criação de novos módulos sem justificar substituição.
9. Seja técnico e objetivo.
10. Não seja genérico.

RELATÓRIO ESTRUTURAL:

{json.dumps(structural_report, indent=2)}
"""

def main():
    engine = SelfInspectionEngine()
    structural_report = engine.run()

    prompt = build_prompt(structural_report)

    print("\n===== ENVIANDO PARA LLM =====\n")
    response = ask_llm(prompt)

    print("\n===== RESPOSTA LLM =====\n")
    print(response)

if __name__ == "__main__":
    main()
