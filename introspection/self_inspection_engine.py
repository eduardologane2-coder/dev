import os
import ast
from pathlib import Path
from collections import defaultdict

BASE_PATH = Path("/srv/dev")
IGNORED_DIRS = {"venv", "__pycache__", "archive", "introspection"}

class SelfInspectionEngine:

    def __init__(self):
        self.python_files = []
        self.import_graph = defaultdict(list)
        self.execution_points = []
        self.entrypoints = []
        self.modules = set()
        self.layer_classification = {}
        self.duplicate_candidates = []
        self.subprocess_users = []

    def scan_files(self):
        for root, dirs, files in os.walk(BASE_PATH):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for file in files:
                if file.endswith(".py"):
                    full_path = Path(root) / file
                    self.python_files.append(full_path)
                    self.modules.add(file.replace(".py", ""))

    def classify_layer(self, module_name):

        # TESTES
        if module_name.startswith("test_"):
            return "TEST_LAYER"

        # EXECUÇÃO
        if "executor" in module_name:
            return "EXECUTION_LAYER"

        # GOVERNANÇA (VALIDATORS, POLICY, CONTRACTS, GATE, GOVERNANCE)
        if (
            "validator" in module_name
            or "policy" in module_name
            or "contract" in module_name
            or "gate" in module_name
            or "governance" in module_name
        ):
            return "GOVERNANCE_LAYER"

        # STRATEGY
        if "strategy" in module_name:
            return "STRATEGY_LAYER"

        # CORE
        if "engine" in module_name:
            return "CORE_ENGINE"

        return "UNKNOWN_LAYER"

    def analyze_file(self, path: Path):
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)
        except Exception:
            return

        module_name = path.stem
        self.layer_classification[module_name] = self.classify_layer(module_name)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.import_graph[module_name].append(alias.name)

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    self.import_graph[module_name].append(node.module)

            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == "run":
                        self.execution_points.append(str(path))

    def run(self):
        self.scan_files()

        for file in self.python_files:
            self.analyze_file(file)

        return {
            "import_graph": dict(self.import_graph),
            "layer_classification": self.layer_classification
        }


if __name__ == "__main__":
    engine = SelfInspectionEngine()
    report = engine.run()
    import json
    print(json.dumps(report, indent=2))
