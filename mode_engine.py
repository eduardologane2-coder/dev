import unicodedata

def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.strip()

PLANEJAMENTO_PREFIXES = (
    "quero",
    "preciso",
    "como",
    "planeje",
    "planejar",
    "planejamento",
)

ANALISE_PREFIXES = (
    "analise",
    "analisar",
    "analisa",
    "avaliar",
    "avalie",
    "examine",
    "examinar",
)

def detect_mode(text: str) -> str:
    t = normalize(text)

    for p in ANALISE_PREFIXES:
        if t.startswith(p):
            return "modo_analise"

    for p in PLANEJAMENTO_PREFIXES:
        if t.startswith(p):
            return "modo_planejamento"

    return "modo_execucao"
