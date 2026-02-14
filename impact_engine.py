from pathlib import Path

def analyze_workspace_impact(workspace_path):
    """
    NÃO executa git.
    Apenas solicita análise.
    """

    return {
        "type": "EXECUTION_REQUEST",
        "origin": "impact_engine",
        "risk": "low",
        "commands": [
            "git status --porcelain"
        ]
    }
