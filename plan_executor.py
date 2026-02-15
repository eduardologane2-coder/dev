from safe_executor import run_safe as execute_request

def execute_plan(request: dict):
    return execute_request(request)
