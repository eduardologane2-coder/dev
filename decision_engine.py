class DecisionEngine:

    def __init__(self):
        self.pending_command = None

    def analyze(self, text: str):
        text = text.strip()

        if text.lower() in ["sim", "confirmar", "execute"]:
            if self.pending_command:
                cmd = self.pending_command
                self.pending_command = None
                return {"action": "execute", "command": cmd}
            else:
                return {"action": "none"}

        # Para desenvolvimento, consideramos toda mensagem como intenção de execução
        self.pending_command = text
        return {
            "action": "propose",
            "command": text
        }
