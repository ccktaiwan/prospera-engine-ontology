import os
import json
import datetime
import subprocess
from pathlib import Path

MONITOR_PATH = Path(os.getenv("PROSPERA_ROOT", str(Path(__file__).resolve().parent.parent))) / "prospera-agent-orchestrator"
LOG_PATH = Path(__file__).resolve().parent / "execution_log.jsonl"


def trigger_monitoring(context=None):
    entry = {"timestamp": datetime.datetime.utcnow().isoformat(), "repo": "prospera-engine-ontology", "context": context or {}}
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    try:
        subprocess.Popen(["python", "monitoring_agent.py"], cwd=str(MONITOR_PATH),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def auto_remediate(error_context=None):
    entry = {"timestamp": datetime.datetime.utcnow().isoformat(),
             "error": str((error_context or {}).get("error", "")),
             "action": "logged", "status": "ATTEMPTED"}
    log = Path(__file__).resolve().parent / "remediation_log.jsonl"
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def log_classification(entity: str, role: str, context: dict = None):
    """Log every classify() call for Internal Intelligence. (L5 ADR-016)"""
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "entity": entity,
        "role": role,
        "context": context or {},
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    trigger_monitoring({"entity": entity, "role": role})
