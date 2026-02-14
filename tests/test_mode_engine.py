from mode_engine import detect_mode

def test_analise_variacoes():
    assert detect_mode("Analise o estado") == "modo_analise"
    assert detect_mode("analisar sistema") == "modo_analise"
    assert detect_mode("Avaliar arquitetura") == "modo_analise"

def test_planejamento_variacoes():
    assert detect_mode("Quero melhorar") == "modo_planejamento"
    assert detect_mode("Como evoluir o sistema?") == "modo_planejamento"

def test_execucao():
    assert detect_mode("mkdir teste") == "modo_execucao"
