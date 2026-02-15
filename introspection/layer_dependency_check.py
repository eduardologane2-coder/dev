import json
from introspection.self_inspection_engine import SelfInspectionEngine

RULES = {

    "INPUT_LAYER": {
        "allowed": [
            "ORCHESTRATION_LAYER"
        ]
    },

    "ORCHESTRATION_LAYER": {
        "allowed": [
            "INPUT_LAYER",
            "INTENTION_LAYER",
            "COGNITIVE_CORE",
            "STRATEGY_LAYER",
            "GOVERNANCE_LAYER",
            "EXECUTION_LAYER",
            "VERSIONING_LAYER",
            "AUDIT_LAYER",
            "LOGGING_LAYER",
            "ORCHESTRATION_LAYER"
        ]
    },

    "COGNITIVE_CORE": {
        "allowed": [
            "COGNITIVE_CORE",
            "STRATEGY_LAYER"
        ]
    },

    "STRATEGY_LAYER": {
        "allowed": [
            "COGNITIVE_CORE",
            "STRATEGY_LAYER"
        ]
    },

    "GOVERNANCE_LAYER": {
        "allowed": [
            "COGNITIVE_CORE",
            "STRATEGY_LAYER",
            "GOVERNANCE_LAYER"
        ]
    },

    "EXECUTION_LAYER": {
        "allowed": [
            "EXECUTION_LAYER"
        ]
    },

    "VERSIONING_LAYER": {
        "allowed": [
            "VERSIONING_LAYER",
            "EXECUTION_LAYER",
            "COGNITIVE_CORE"
        ]
    },

    "AUDIT_LAYER": {
        "allowed": [
            "AUDIT_LAYER",
            "VERSIONING_LAYER",
            "COGNITIVE_CORE"
        ]
    },

    "LOGGING_LAYER": {
        "allowed": [
            "LOGGING_LAYER",
            "COGNITIVE_CORE"
        ]
    },

    "TEST_LAYER": {
        "allowed": [
            "TEST_LAYER",
            "COGNITIVE_CORE",
            "STRATEGY_LAYER",
            "GOVERNANCE_LAYER",
            "EXECUTION_LAYER",
            "VERSIONING_LAYER",
            "AUDIT_LAYER",
            "LOGGING_LAYER",
            "ORCHESTRATION_LAYER"
        ]
    }
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

    if violations:
        print("\nVIOLAÇÕES DETECTADAS:\n")
        print(json.dumps(violations, indent=2))
    else:
        print("\nNenhuma violação arquitetural detectada.\n")

if __name__ == "__main__":
    check_dependencies()
