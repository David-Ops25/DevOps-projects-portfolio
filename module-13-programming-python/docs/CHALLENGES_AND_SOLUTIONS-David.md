# Challenges faced and how they were solved

## 1) Python venv creation failed (`ensurepip is not available`)
**Symptom:** `python3 -m venv .venv` failed on Ubuntu/Debian with an `ensurepip` error.  
**Fix:** Install the venv package and retry:
```bash
sudo apt install python3-venv
python3 -m venv .venv
```

## 2) CLI commands were not found after writing code
**Symptom:** `release-notes: command not found` / `gitlab-audit: command not found`.  
**Cause:** the packages weren’t installed (so the console scripts weren’t registered).  
**Fix:** install each project in editable mode:
```bash
pip install -e projects/<project_name>
```

## 3) Shell got “stuck” at a `>` prompt
**Symptom:** the terminal showed `>` and wouldn’t run normal commands.  
**Cause:** an unfinished heredoc / multiline paste.  
**Fix:** exit with `Ctrl+C`, then re-run commands using safer one-liners.
(For documentation generation, prefer writing files from a single command.)

## 4) CI reliability for API-based project
**Symptom:** tests that call the real GitLab API are flaky and require internet.  
**Fix:** use mocked HTTP responses (via `unittest.mock`) so the test suite is deterministic and CI-safe.

## 5) Default branch detection for README checks
**Symptom:** some repos use `main`, some `master`, others custom.  
**Fix:** try `default_branch` first, then fall back to `main` and `master`.
