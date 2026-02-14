import json
from pathlib import Path

METRICS_FILE = Path("/srv/dev/metrics.json")

def metrics_status():
    if not METRICS_FILE.exists():
        return "📊 Nenhuma métrica registrada ainda."

    data = json.loads(METRICS_FILE.read_text())

    return (
        "📊 MÉTRICAS DO DEV\n\n"
        f"Execuções: {data.get('executions',0)}\n"
        f"Commits: {data.get('commits',0)}\n"
        f"SelfMods: {data.get('selfmods',0)}\n"
        f"Falhas: {data.get('failures',0)}\n"
        f"Rollbacks: {data.get('rollbacks',0)}\n"
        f"Última atualização: {data.get('last_update')}"
    )
