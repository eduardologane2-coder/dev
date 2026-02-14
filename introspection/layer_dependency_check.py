import json
from introspection.self_inspection_engine import SelfInspectionEngine

RULES = {
    "CORE_ENGINE": {"allowed": ["CORE_ENGINE", "STRATEGY_LAYER"]},
    "GOVERNANCE_LAYER": {"allowed": ["GOVERNANCE_LAYER", "CORE_ENGINE", "STRATEGY_LAYER"]},
    "EXECUTION_LAYER": {"allowed": ["EXECUTION_LAYER", "GOVERNANCE_LAYER", "CORE_ENGINE", "STRATEGY_LAYER"]},
    "STRATEGY_LAYER": {"allowed": ["STRATEGY_LAYER", "CORE_ENGINE"]},
    "TEST_LAYER": {"allowed": ["CORE_ENGINE", "GOVERNANCE_LAYER", "EXECUTION_LAYER", "STRATEGY_LAYER", "TEST_LAYER"]},
    "UNKNOWN_LAYER": {"allowed": ["CORE_ENGINE", "GOVERNANCE_LAYER", "EXECUTION_LAYER", "STRATEGY_LAYER", "TEST_LAYER", "UNKNOWN_LAYER"]}
}

def check_dependencies():
    engine = SelfInspectionEngine()
    report = engine.run()

    layer_map = report["layer_classification"]
    import_graph = report["import_graph"]

    violations = []

    for module, imports in import_graph.items():
        module_layer = layer_map.get(module, "UNKNOWN_LAYER")

        for imported in imports:
            imported_module = imported.split(".")[0]
            imported_layer = layer_map.get(imported_module)

            if not imported_layer:
                continue

            allowed_layers = RULES.get(module_layer, {}).get("allowed", [])

            if imported_layer not in allowed_layers:
                violations.append({
                    "module": module,
                    "module_layer": module_layer,
                    "imports": imported_module,
                    "import_layer": imported_layer
                })

    return violations

if __name__ == "__main__":
    violations = check_dependencies()

    if not violations:
        print("\nNenhuma violação de camada detectada.\n")
    else:
        print("\nVIOLAÇÕES DETECTADAS:\n")
        print(json.dumps(violations, indent=2))
