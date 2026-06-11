# ── Prospera SYSTEM HEADER (ADR-0032/SBOM) ──
# 性質:engineering ｜設計:Kevin 架構 ｜執行:AI 工具(claude.ai+Claude Code)
# 驗證:無機制驗證 ｜IP:創造性歸 Kevin(發明人), AI 為執行工具 (ADR-0032)
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
    "prospera-client-phoenix":       {"role": "EXECUTION", "ring": "R5", "workflow": "content"},
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


# ─── SME Stage Classification (ADR-021) ─────────────────────────────────────

SME_STAGE_ONTOLOGY = {
    "stage_1": {
        "name": "Digital Foundation",
        "criteria": ["brand_config_exists", "content_template_exists"],
        "capabilities": ["content", "strategy"],
        "workflow_priority": "content",
    },
    "stage_2": {
        "name": "Content Engine",
        "criteria": ["monthly_content_plan", "active_platform"],
        "capabilities": ["content", "strategy", "gengrant"],
        "workflow_priority": "strategy",
    },
    "stage_3": {
        "name": "Analytics and Ads",
        "criteria": ["analytics_connected", "monthly_inquiries_tracked", "paid_channel_active"],
        "capabilities": ["content", "strategy", "analytics", "gengrant"],
        "workflow_priority": "analytics",
    },
    "stage_4": {
        "name": "Lead Generation",
        "criteria": ["inquiry_conversion_5pct", "crm_basics"],
        "capabilities": ["content", "strategy", "analytics", "gengrant", "crm"],
        "workflow_priority": "analytics",
    },
    "stage_5": {
        "name": "Automation",
        "criteria": ["booking_system", "automated_followup"],
        "capabilities": ["content", "strategy", "analytics", "gengrant", "crm", "automation"],
        "workflow_priority": "automation",
    },
}

CLIENT_STAGE_REGISTRY = {
    "phoenix": {
        "current_stage": 2,
        "stage_name": "Content Engine",
        "tenant_id": "phoenix",
        "client_name": "phoenix lucky health center",
        "industry": "health_management",
        "blockers": ["ga4_not_connected", "ads_budget_unconfirmed"],
    },
    "xinyuan": {
        "current_stage": 1,
        "stage_name": "Digital Foundation",
        "tenant_id": "xinyuan",
        "client_name": "xinyuan interior engineering",
        "industry": "interior_renovation",
        "blockers": ["website_not_live", "no_active_platform"],
    },
}


def classify_sme_stage(tenant_id: str) -> dict:
    """Classify a client's current SME Stage and return advancement recommendations."""
    client = CLIENT_STAGE_REGISTRY.get(tenant_id)
    if not client:
        return {"error": f"tenant_id '{tenant_id}' not in CLIENT_STAGE_REGISTRY"}
    stage_num = client["current_stage"]
    stage_key = f"stage_{stage_num}"
    stage_info = SME_STAGE_ONTOLOGY.get(stage_key, {})
    next_stage_key = f"stage_{stage_num + 1}"
    next_stage = SME_STAGE_ONTOLOGY.get(next_stage_key, {})
    return {
        "tenant_id": tenant_id,
        "current_stage": stage_num,
        "stage_name": stage_info.get("name", "unknown"),
        "available_capabilities": stage_info.get("capabilities", []),
        "workflow_priority": stage_info.get("workflow_priority", "content"),
        "blockers": client.get("blockers", []),
        "next_stage": stage_num + 1 if next_stage else None,
        "next_stage_name": next_stage.get("name"),
        "next_stage_criteria": next_stage.get("criteria", []),
        "advancement_gap": [c for c in next_stage.get("criteria", []) if c in client.get("blockers", [])],
    }


def classify_entity(entity: str) -> dict:
    """Unified entry point: classify repo, request, or SME tenant."""
    if entity in CLIENT_STAGE_REGISTRY:
        return classify_sme_stage(entity)
    result = classify_repo(entity)
    if not result.get("found"):
        result2 = classify_request(entity)
        if result2.get("found"):
            return result2
    return result
