import os
import ast
from pathlib import Path
from collections import defaultdict

BASE_PATH = Path("/srv/dev")
IGNORED_DIRS = {"venv", "__pycache__", "archive", "introspection", "sandbox", "workspaces"}

class SelfInspectionEngine:

    def __init__(self):
        self.python_files = []
        self.import_graph = defaultdict(list)
        self.modules = set()
        self.layer_classification = {}

    def scan_files(self):
        for root, dirs, files in os.walk(BASE_PATH):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for file in files:
                if file.endswith(".py"):
                    full_path = Path(root) / file
                    self.python_files.append(full_path)
                    self.modules.add(file.replace(".py", ""))

    def classify_layer(self, module_name):

        if module_name.startswith("test_"):
            return "TEST_LAYER"

        if module_name in ["executor", "dev_executor", "plan_executor"]:
            return "EXECUTION_LAYER"

        if module_name in ["versioning", "git_auto_commit"]:
            return "VERSIONING_LAYER"

        if module_name in ["architecture_audit"]:
            return "AUDIT_LAYER"

        if module_name in ["joseph_sync"] or module_name.endswith("_contract") or module_name.startswith("selfmod_"):
            return "GOVERNANCE_LAYER"

        if module_name.startswith("strategy_"):
            return "STRATEGY_LAYER"

        if module_name.endswith("_engine"):
            return "CORE_ENGINE"

        if module_name in ["orchestrator", "dev_bot"]:
            return "ORCHESTRATION_LAYER"

        return "CORE_ENGINE"

    def build_import_graph(self):
        for file_path in self.python_files:
            module_name = file_path.stem
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    tree = ast.parse(f.read())
                except:
                    continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.import_graph[module_name].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.import_graph[module_name].append(node.module)

    def run(self):
        self.scan_files()
        for module in self.modules:
            self.layer_classification[module] = self.classify_layer(module)
        self.build_import_graph()

        return {
            "layer_classification": self.layer_classification,
            "import_graph": self.import_graph
        }
