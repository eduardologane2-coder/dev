import json
from datetime import datetime
from pathlib import Path
from introspection.self_inspection_engine import SelfInspectionEngine
from llm_engine import ask_llm

AUDIT_DIR = Path("/srv/dev/introspection/audit_history")

def build_prompt(structural_report: dict) -> str:
    return f"""
Você está realizando auditoria técnica estrutural completa do sistema Dev.

OBJETIVO:
- Identificar riscos arquiteturais reais
- Detectar acoplamentos perigosos
- Detectar mistura de camadas
- Avaliar maturidade arquitetural (0-10)
- Sugerir evolução mínima
- Não propor revoluções
- Não propor criação de novos módulos sem justificar substituição

RELATÓRIO ESTRUTURAL:
{json.dumps(structural_report, indent=2)}

Seja técnico. Seja direto. Não seja genérico.
"""

def run_audit():
    engine = SelfInspectionEngine()
    structural_report = engine.run()

    prompt = build_prompt(structural_report)

    response = ask_llm(prompt)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = AUDIT_DIR / f"audit_{timestamp}.json"

    result = {
        "timestamp": timestamp,
        "structural_report": structural_report,
        "llm_analysis": response
    }

    output_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    return output_file

if __name__ == "__main__":
    file_path = run_audit()
    print(f"\nAuditoria salva em: {file_path}\n")
