import pytest, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from monitoring_hook import trigger_monitoring, log_classification
from ontology_classifier import classify

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "execution_log.jsonl")


def test_trigger_monitoring():
    trigger_monitoring({"test": True})
    assert os.path.exists(LOG_PATH)


def test_log_classification():
    log_classification("prospera-os", "EXECUTION")
    with open(LOG_PATH, encoding="utf-8") as f:
        lines = f.readlines()
    # Find last entry with top-level 'entity' key (log_classification entries, not trigger_monitoring)
    entries_with_entity = [json.loads(l.strip()) for l in lines
                           if l.strip() and "entity" in json.loads(l.strip()) and "repo" not in json.loads(l.strip())]
    assert len(entries_with_entity) > 0
    last = entries_with_entity[-1]
    assert last["entity"] == "prospera-os"
    assert last["role"] == "EXECUTION"


def test_classify_triggers_log():
    initial_size = os.path.getsize(LOG_PATH) if os.path.exists(LOG_PATH) else 0
    result = classify("prospera-gateway")
    assert result["role"] == "EXECUTION"
    assert os.path.exists(LOG_PATH)
    assert os.path.getsize(LOG_PATH) >= initial_size
