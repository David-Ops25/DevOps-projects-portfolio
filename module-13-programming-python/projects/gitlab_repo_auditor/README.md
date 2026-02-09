# GitLab Repo Auditor

A CLI that audits a GitLab user's public repositories and outputs:
- `audit.md` (human-friendly report)
- `audit.json` (automation-friendly output)

## What problem it solves
When evaluating repos (your own or someone else's) you often want a quick health check:
- Is there a README?
- How active is the repo?
- Stars/forks signals (lightweight)

This tool generates a Markdown report for humans and JSON for automation.

## Install (editable)
From the repo root:
```bash
pip install -e projects/gitlab_repo_auditor
```

## Run
```bash
gitlab-audit --username gitlab --output-dir out
```

## Tests
The test suite uses mocked HTTP calls so CI does not require internet access:
```bash
pytest -q projects/gitlab_repo_auditor/tests
```
