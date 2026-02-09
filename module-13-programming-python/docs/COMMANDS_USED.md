# Commands used (Module 13)

> Copy/paste friendly. Assumes repo root and an activated venv.

## System setup (Ubuntu/Debian)
If `python3 -m venv` fails with `ensurepip is not available`:
```bash
sudo apt update
sudo apt install python3-venv
```

## Create & activate venv
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip wheel
```

## Install dev tools
```bash
pip install -r requirements-dev.txt
```

## Install each project (editable)
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

## Lint & tests
```bash
ruff check .
pytest
```
