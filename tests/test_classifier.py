import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ontology_classifier import classify, classify_repo, classify_request, get_workflow_for_role


def test_classify_execution_repo():
    r = classify("prospera-os")
    assert r["role"] == "EXECUTION"
    assert r["ring"] == "R1"


def test_classify_spec_repo():
    r = classify("prospera-blueprint-esg")
    assert r["role"] == "SPEC"


def test_classify_external_signal_repo():
    r = classify("prospera-engine-external-intelligence")
    assert r["role"] == "EXTERNAL_SIGNAL"


def test_classify_user_intent_request():
    r = classify("content", entity_type="request")
    assert r["role"] == "USER_INTENT"
    assert r["type"] == "Dynamic Workflow"


def test_classify_world_intent_request():
    r = classify("subsidy", entity_type="request")
    assert r["role"] == "WORLD_INTENT"
    assert r["type"] == "External Intelligence"


def test_workflow_routing():
    assert get_workflow_for_role("EXECUTION") == "agent_workflow"
    assert get_workflow_for_role("SPEC") == "spec_integrity_check"
    assert get_workflow_for_role("WORLD_INTENT") == "external_intelligence_pipeline"


def test_auto_classify():
    assert classify("prospera-gateway")["role"] == "EXECUTION"
    assert classify("gengrant")["role"] == "USER_INTENT"
