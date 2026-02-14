import subprocess

def execute_plan(plan):
    results = []

    if isinstance(plan, str):
        return [{"success": False, "error": "Plano textual não executável."}]

    for step in plan:
        result = subprocess.run(step, shell=True, capture_output=True, text=True)
        results.append({
            "command": step,
            "success": result.returncode == 0,
            "output": result.stdout + result.stderr
        })

        if result.returncode != 0:
            break

    return results
