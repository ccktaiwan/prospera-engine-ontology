# DEVELOPMENT_PLAN | prospera-engine-ontology
Date: 2026-06-03
Type: ENGINE
Ring: R4a
Level: L5 (declared)

## Ecosystem Role
語意分類器。Decision Layer 的語意基礎。classify(entity) API 讓系統知道每個 repo 或
請求類型的角色（EXECUTION/SPEC/EXTERNAL_SIGNAL）和對應 workflow。
對應業界：Uber Schemaless / Netflix Metacat。ADR-016 執行化已完成。

## Real Current Capability
- ontology_classifier.py: complete REPO_ONTOLOGY (30+ repos mapped), REQUEST_ONTOLOGY (10 request types), WORKFLOW_ROUTING dict
- classify(entity) returns {role, ring, workflow} synchronously
- classify_request(request_type) routes to agent by workflow type
- route_workflow(ontology_role, intent) dispatches to agent_workflow / spec_integrity_check / external_intelligence_pipeline
- kpi_checker.py: classification accuracy tracking
- monitoring_hook.py: L5 monitoring
- spec_health_check.py: validates reference integrity (this repo as SPEC checker)
- Tests: test_classifier.py, test_monitoring.py, test_kpi_checker.py, test_l5.py, test_contract.py

## Gap Analysis
- BIGGEST GAP: No HTTP service wrapper — classify() can only be imported, not called via REST API
- Decision Engine in prospera-os cannot call this remotely (must import directly, creating coupling)
- route_workflow() dispatches to external_intelligence_pipeline() but that function is undefined/imported from where?
- No dynamic ontology update mechanism — REPO_ONTOLOGY is hardcoded dict (new repos require code change)
- No fallback for unknown entities (returns KeyError rather than graceful UNKNOWN response)

## Next 3 Development Tasks

### Task 1: Add HTTP service wrapper
- What: Create ontology_service.py (FastAPI app, port 8082) exposing GET /classify?entity={name} and GET /classify-request?type={type}; returns JSON {role, ring, workflow}; add /health endpoint
- Acceptance: python ontology_service.py starts on port 8082; curl localhost:8082/classify?entity=prospera-os returns {"role":"EXECUTION","ring":"R0","workflow":"mcp_server"}
- Session: session_44

### Task 2: Graceful unknown entity handling
- What: Update classify() to return {"role": "UNKNOWN", "ring": "UNREGISTERED", "workflow": "manual_review"} for unrecognized entities instead of KeyError; log unknown entities to unknown_entities.jsonl
- Acceptance: classify("new-repo-xyz") returns UNKNOWN dict; unknown_entities.jsonl records the query; test_classifier.py has test for unknown entity
- Session: session_44

### Task 3: Dynamic ontology update via JSON config
- What: Create ontology_registry.json as the source of truth for REPO_ONTOLOGY; update ontology_classifier.py to load from this file at startup (not hardcoded); provide update_ontology.py script for adding new repos
- Acceptance: Adding a new entry to ontology_registry.json and restarting service makes classify("new-entry") return correct result without code change
- Session: session_45
