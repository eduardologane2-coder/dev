#!/usr/bin/env python3
import json
import sys
from pathlib import Path

CHECKLIST = Path("/srv/dev/strategic_checklist.json")

def fail(msg, details=None):
    out = {"ok": False, "error": msg, "details": details or {}}
    print(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(2)

def ok(payload):
    payload["ok"] = True
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    sys.exit(0)

def read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"JSON inválido: {p}", {"exception": str(e)})

def file_contains(path: Path, needles):
    txt = path.read_text(encoding="utf-8", errors="replace")
    missing = [n for n in needles if n not in txt]
    return missing

def validate_step(step):
    v = step.get("validators", {})
    evidence = {"step_id": step["id"], "step_name": step["name"], "checks": []}

    # files_must_exist
    for f in v.get("files_must_exist", []):
        p = Path(f)
        if not p.exists():
            fail("Arquivo obrigatório não existe", {"file": str(p), "step": step["id"]})
        evidence["checks"].append({"type": "exists", "file": str(p), "ok": True})

    # json_must_have_keys
    for file, keys in v.get("json_must_have_keys", {}).items():
        p = Path(file)
        data = read_json(p)
        missing = [k for k in keys if k not in data]
        if missing:
            fail("strategy.json sem chaves obrigatórias", {"file": str(p), "missing": missing, "step": step["id"]})
        evidence["checks"].append({"type": "json_keys", "file": str(p), "ok": True})

    # json_must_be_list
    for f in v.get("json_must_be_list", []):
        p = Path(f)
        data = read_json(p)
        if not isinstance(data, list):
            fail("Arquivo JSON deveria ser uma lista", {"file": str(p), "type": str(type(data)), "step": step["id"]})
        evidence["checks"].append({"type": "json_list", "file": str(p), "ok": True})

    # python_must_contain
    for file, needles in v.get("python_must_contain", {}).items():
        p = Path(file)
        if not p.exists():
            fail("Arquivo python esperado não existe", {"file": str(p), "step": step["id"]})
        missing = file_contains(p, needles)
        if missing:
            fail("Arquivo python não contém marcadores obrigatórios", {"file": str(p), "missing": missing, "step": step["id"]})
        evidence["checks"].append({"type": "contains", "file": str(p), "ok": True})

    return evidence

def advance_checklist(checklist):
    steps = checklist["steps"]
    cur = checklist.get("current_step", 1)

    # acha step atual pendente
    step = next((s for s in steps if s["id"] == cur), None)
    if not step:
        fail("current_step inválido", {"current_step": cur})

    if step["status"] == "done":
        ok({"message": "Step já estava concluído", "current_step": cur})

    evidence = validate_step(step)

    # marca done e avança
    step["status"] = "done"
    # avança para próximo pending
    next_pending = next((s["id"] for s in steps if s["status"] != "done"), None)
    checklist["current_step"] = next_pending if next_pending else cur

    CHECKLIST.write_text(json.dumps(checklist, indent=2, ensure_ascii=False), encoding="utf-8")

    ok({
        "message": "VALIDADO E AVANÇADO",
        "validated_step": cur,
        "next_step": checklist["current_step"],
        "evidence": evidence
    })

def main():
    if not CHECKLIST.exists():
        fail("Checklist não existe", {"path": str(CHECKLIST)})

    checklist = read_json(CHECKLIST)
    advance_checklist(checklist)

if __name__ == "__main__":
    main()
