"""
ontology_classifier.py | Ring R4a Internal Intelligence | v1.0
ADR-016: Ontology Engine 執行化
classify(entity) API — 讓 Decision Layer 知道每個 entity 的語意角色
對應業界：Uber Schemaless / Netflix Metacat
"""
import os
import json

REPO_ONTOLOGY = {
    "prospera-os":                          {"role": "EXECUTION", "ring": "R1", "workflow": "mcp_server"},
    "prospera-gateway":                     {"role": "EXECUTION", "ring": "R6", "workflow": "gateway_route"},
    "prospera-product-exam":                {"role": "EXECUTION", "ring": "R5", "workflow": "exam"},
    "prospera-product-consulting":          {"role": "EXECUTION", "ring": "R5", "workflow": "content"},
    "prospera-product-gengrant":            {"role": "EXECUTION", "ring": "R5", "workflow": "gengrant"},
    "prospera-agent-orchestrator":          {"role": "EXECUTION", "ring": "R7", "workflow": "orchestrate"},
    "prospera-engine-external-intelligence":{"role": "EXTERNAL_SIGNAL", "ring": "R4b", "workflow": "signal_collect"},
    "prospera-constitution-governance":     {"role": "SPEC", "ring": "R0", "workflow": "spec_integrity"},
    "prospera-constitution-kernel":         {"role": "SPEC", "ring": "R1", "workflow": "spec_integrity"},
    "prospera-constitution-identity":       {"role": "SPEC", "ring": "R1", "workflow": "spec_integrity"},
    "prospera-standard-engineering":        {"role": "SPEC", "ring": "R2", "workflow": "spec_integrity"},
    "prospera-standard-compliance":         {"role": "SPEC", "ring": "R2", "workflow": "spec_integrity"},
    "prospera-standard-audit":              {"role": "SPEC", "ring": "R2", "workflow": "spec_integrity"},
    "prospera-standard-ip":                 {"role": "SPEC", "ring": "R2", "workflow": "spec_integrity"},
    "prospera-blueprint-esg":               {"role": "SPEC", "ring": "R3", "workflow": "spec_integrity"},
    "prospera-blueprint-mobile":            {"role": "SPEC", "ring": "R3", "workflow": "spec_integrity"},
    "prospera-blueprint-ip":                {"role": "SPEC", "ring": "R3", "workflow": "spec_integrity"},
    "prospera-blueprint-stablecoin":        {"role": "SPEC", "ring": "R3", "workflow": "spec_integrity"},
    "prospera-engine-generation":           {"role": "EXECUTION", "ring": "R4a", "workflow": "generate"},
    "prospera-engine-workflow":             {"role": "EXECUTION", "ring": "R4a", "workflow": "workflow_route"},
    "prospera-engine-ontology":             {"role": "EXECUTION", "ring": "R4a", "workflow": "classify"},
    "prospera-engine-token":                {"role": "SPEC", "ring": "R4a", "workflow": "spec_integrity"},
    "prospera-engine-api":                  {"role": "EXECUTION", "ring": "R4a", "workflow": "api_route"},
    "prospera-engine-registry":             {"role": "SPEC", "ring": "R6", "workflow": "spec_integrity"},
    "prospera-agent-memory":                {"role": "EXECUTION", "ring": "R7", "workflow": "snapshot"},
    "prospera-product-dashboard":           {"role": "EXECUTION", "ring": "R5", "workflow": "dashboard"},
    "prospera-product-phoenix-lucky":       {"role": "EXECUTION", "ring": "R5", "workflow": "content"},
    "prospera-product-esg":                 {"role": "EXECUTION", "ring": "R5", "workflow": "content"},
    "prospera-product-client-template":     {"role": "SPEC", "ring": "R5", "workflow": "spec_integrity"},
    "prospera-infra-ci":                    {"role": "SPEC", "ring": "R6", "workflow": "spec_integrity"},
    "prospera-infra-compliance":            {"role": "SPEC", "ring": "R6", "workflow": "spec_integrity"},
}

REQUEST_ONTOLOGY = {
    "content":   {"role": "USER_INTENT",  "type": "Dynamic Workflow", "agent": "ContentAgent"},
    "strategy":  {"role": "USER_INTENT",  "type": "Dynamic Workflow", "agent": "StrategyAgent"},
    "analytics": {"role": "USER_INTENT",  "type": "Dynamic Workflow", "agent": "AnalyticsAgent"},
    "exam":      {"role": "USER_INTENT",  "type": "Dynamic Workflow", "agent": "ExamAgent"},
    "gengrant":  {"role": "USER_INTENT",  "type": "Dynamic Workflow", "agent": "GrantAgent"},
    "crawl":     {"role": "USER_INTENT",  "type": "Dynamic Workflow", "agent": "CrawlerAgent"},
    "classify":  {"role": "USER_INTENT",  "type": "Dynamic Workflow", "agent": "OntologyAgent"},
    "signal_collect": {"role": "EXTERNAL_SIGNAL", "type": "External Intelligence", "agent": "SubsidySignalAgent"},
    "subsidy":   {"role": "WORLD_INTENT", "type": "External Intelligence", "agent": "SubsidySignalAgent"},
    "trend":     {"role": "WORLD_INTENT", "type": "External Intelligence", "agent": "TrendSignalAgent"},
    "policy":    {"role": "WORLD_INTENT", "type": "External Intelligence", "agent": "PolicySignalAgent"},
}

WORKFLOW_ROUTING = {
    "EXECUTION":       "agent_workflow",
    "SPEC":            "spec_integrity_check",
    "EXTERNAL_SIGNAL": "external_intelligence_pipeline",
    "USER_INTENT":     "dynamic_task_agent",
    "WORLD_INTENT":    "external_intelligence_pipeline",
}


def classify_repo(repo_name: str) -> dict:
    ontology = REPO_ONTOLOGY.get(repo_name)
    if ontology:
        return {"entity": repo_name, "entity_type": "repo", **ontology, "found": True}
    if any(k in repo_name for k in ["blueprint", "standard", "constitution"]):
        return {"entity": repo_name, "entity_type": "repo", "role": "SPEC",
                "ring": "unknown", "workflow": "spec_integrity", "found": False}
    return {"entity": repo_name, "entity_type": "repo", "role": "EXECUTION",
            "ring": "unknown", "workflow": "unknown", "found": False}


def classify_request(workflow: str) -> dict:
    ontology = REQUEST_ONTOLOGY.get(workflow)
    if ontology:
        return {"entity": workflow, "entity_type": "request", **ontology, "found": True}
    return {"entity": workflow, "entity_type": "request", "role": "USER_INTENT",
            "type": "Dynamic Workflow", "agent": "unknown", "found": False}


def classify(entity: str, entity_type: str = "auto") -> dict:
    """
    Main API: classify any entity by its Ontology Role.
    entity_type: 'repo' | 'request' | 'auto'
    Returns: role (EXECUTION|SPEC|EXTERNAL_SIGNAL|USER_INTENT|WORLD_INTENT)
    """
    if entity_type == "repo" or (entity_type == "auto" and "prospera-" in entity):
        result = classify_repo(entity)
    else:
        result = classify_request(entity)
    # L5: log every classification call (ADR-016)
    try:
        from monitoring_hook import log_classification
        log_classification(entity, result.get("role", "?"))
    except Exception:
        pass
    return result


def get_workflow_for_role(role: str) -> str:
    return WORKFLOW_ROUTING.get(role, "unknown")


if __name__ == "__main__":
    tests = ["prospera-os", "prospera-blueprint-esg", "prospera-engine-external-intelligence",
             "content", "gengrant", "subsidy"]
    for t in tests:
        result = classify(t)
        print(f"{t}: {result['role']} -> {get_workflow_for_role(result['role'])}")
