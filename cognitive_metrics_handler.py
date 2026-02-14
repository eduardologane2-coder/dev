from cognitive_metrics_engine import load

def cognitive_metrics_status():
    data = load()
    return f"""
🧠 MÉTRICAS COGNITIVAS

Total decisões: {data["total"]}
EXECUTE: {data["EXECUTE"]}
PLAN: {data["PLAN"]}
REJECT: {data["REJECT"]}
CONFIRM: {data["CONFIRM"]}
BRIEFING: {data["BRIEFING"]}
Confiança média: {round(data["avg_confidence"], 3)}
Última atualização: {data["last_update"]}
"""
