import os, json, datetime, subprocess as _sp
from pathlib import Path

REPO_NAME = 'prospera-engine-ontology'
EXEC_REPOS = ['prospera-os','prospera-gateway','prospera-product-exam',
              'prospera-product-consulting','prospera-product-gengrant',
              'prospera-agent-orchestrator']
GITHUB_ROOT = r'C:\AI_WorkDir\GitHub'

def check_reference_integrity() -> dict:
    referenced = False
    for exec_repo in EXEC_REPOS:
        repo_path = Path(GITHUB_ROOT) / exec_repo
        if not repo_path.exists():
            continue
        for py_file in repo_path.rglob('*.py'):
            try:
                if REPO_NAME in py_file.read_text(encoding='utf-8', errors='ignore'):
                    referenced = True
                    break
            except Exception:
                continue
        if referenced:
            break
    return {'repo': REPO_NAME, 'referenced': referenced,
            'status': 'REFERENCED' if referenced else 'ORPHANED'}

def check_version_consistency() -> dict:
    base = Path(__file__).resolve().parent
    has_contract = (base / 'CONTRACT.md').exists()
    has_agents = (base / 'AGENTS.md').exists()
    return {'contract': has_contract, 'agents': has_agents,
            'status': 'CONSISTENT' if (has_contract and has_agents) else 'INCONSISTENT'}

def check_activity() -> dict:
    result = _sp.run(
        ['git', 'log', '--since=30 days ago', '--oneline'],
        capture_output=True,
        cwd=str(Path(__file__).resolve().parent),
        encoding='utf-8', errors='replace'
    )
    active = bool(result.stdout.strip())
    return {'active': active, 'status': 'ACTIVE' if active else 'STALE'}

def run_spec_health() -> dict:
    report = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'repo': REPO_NAME,
        'type': 'SPEC',
        'reference': check_reference_integrity(),
        'version': check_version_consistency(),
        'activity': check_activity()
    }
    log_path = Path(__file__).resolve().parent / 'spec_health.json'
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report

if __name__ == '__main__':
    print(json.dumps(run_spec_health(), ensure_ascii=False, indent=2))
