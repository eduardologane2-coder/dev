import subprocess

def execute_plan(plan_steps):
    results = []

    for step in plan_steps:
        result = subprocess.run(
            step,
            shell=True,
            capture_output=True,
            text=True
        )

        results.append({
            "step": step,
            "success": result.returncode == 0,
            "output": result.stdout + result.stderr
        })

        if result.returncode != 0:
            break

    return results
