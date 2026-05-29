# CLAUDE.md — Prospera governance contract

**Authority**: ccktaiwan
**Schema**: prospera-os/DIRECTORY_SCHEMA.json
**Skills**: prospera-infra-ci/skills/SKILL-CORE.md
**Canonical source**: system_index.yaml v3.0

---

## EXECUTION MODEL

When working in any Prospera repo:
- NEVER produce manual scripts for the human to run
- ALWAYS use Claude Code to directly create files, run git, move directories
- If a task needs a decision → ask ccktaiwan ONE question, then execute
- The human judges. Claude Code executes.

---

## This repo

**Repo**: prospera-engine-ontology
**Status**: ACTIVE
**Tier**: L4 (Engine)
**Ring**: Ring 4 — Engines

**Contract**:
- INPUT: Knowledge query + entity relationship
- OUTPUT: Ontology graph + structured knowledge

**Purpose**: Knowledge graph, ontology, semantic layer
