import json
from datetime import datetime
from pathlib import Path

DEV_DIR = Path("/srv/dev")
STRATEGY_FILE = DEV_DIR / "strategy.json"

def decompose_task(command: str):
    """
    Transforma uma intenção vaga em subtarefas técnicas estruturadas.
    """
    subtasks = []

    if "melhorar" in command or "refatorar" in command:
        subtasks = [
            "Analisar código atual",
            "Mapear impacto",
            "Propor melhoria técnica",
            "Implementar alteração",
            "Testar comportamento",
            "Validar impacto estratégico"
        ]
    elif "criar" in command:
        subtasks = [
            "Definir estrutura necessária",
            "Criar arquivos base",
            "Implementar lógica inicial",
            "Testar funcionamento",
            "Registrar decisão estratégica"
        ]
    else:
        subtasks = [
            "Executar comando diretamente",
            "Validar resultado",
            "Registrar impacto"
        ]

    return {
        "original_command": command,
        "generated_at": str(datetime.now()),
        "subtasks": subtasks
    }
