# Module 13 — Python for DevOps (Portfolio Projects)

A portfolio-grade set of Python projects designed around DevOps-style workflows:
CLI tools, automation outputs (JSON/Markdown), tests, and CI-friendly structure.

## What this module is about

Module 13 focuses on Python fundamentals that are directly useful for DevOps work:
- building CLI tools (repeatable workflows)
- automating routine tasks (files/spreadsheets)
- consuming external APIs (reporting/auditing)
- writing tests and keeping CI stable

## Projects

### 1) Countdown CLI
**Problem:** Track deadlines consistently (timezone-safe) and optionally emit automation-friendly JSON.  
**Outputs:** terminal text or JSON.

Location: `projects/countdown_cli/`

### 2) Release Notes Generator
**Problem:** Convert a changelog spreadsheet into readable release notes + a JSON summary for pipelines.  
**Outputs:** `release_notes.md`, `summary.json`

Location: `projects/release_notes_generator/`

### 3) GitLab Repo Auditor
**Problem:** Audit public repos for hygiene signals (README presence, activity, stars/forks) and export a report.  
**Outputs:** `audit.md`, `audit.json`  
**Testing:** includes mocked HTTP tests so CI does not need internet.

Location: `projects/gitlab_repo_auditor/`

## Quickstart

### Create & activate a venv
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Install dev tooling
```bash
pip install -r requirements-dev.txt
```

### Install projects (editable)
```bash
pip install -e projects/countdown_cli
pip install -e projects/release_notes_generator
pip install -e projects/gitlab_repo_auditor
```

## Run examples

### Countdown CLI
```bash
countdown --goal "Demo" --deadline "2026-03-01T12:00:00Z" --timezone "Europe/London"
countdown --goal "Demo" --deadline "2026-03-01T12:00:00Z" --json
```

### Release Notes Generator
```bash
release-notes --input projects/release_notes_generator/sample/changelog.csv   --output-dir projects/release_notes_generator/out --version 0.1.0
```

### GitLab Repo Auditor
```bash
gitlab-audit --username gitlab --output-dir projects/gitlab_repo_auditor/out
```

## Quality gates

### Lint
```bash
ruff check .
```

### Tests
```bash
pytest
```

## Documentation
- Commands used: `docs/COMMANDS_USED.md`
- Challenges & solutions: `docs/CHALLENGES_AND_SOLUTIONS.md`

## CI
GitHub Actions workflow: `.github/workflows/ci.yml`
