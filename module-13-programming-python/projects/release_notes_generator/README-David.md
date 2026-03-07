# Release Notes Generator

Generate `release_notes.md` and `summary.json` from a CSV/XLSX changelog.

## What problem it solves
In teams, changelogs often live in spreadsheets. This tool converts that spreadsheet into:
- clean, readable release notes for stakeholders
- a structured JSON summary for automation (dashboards, pipelines)

## Install (editable)
From the repo root:
```bash
pip install -e projects/release_notes_generator
```

## Run
```bash
release-notes --input sample/changelog.csv --output-dir out --version 0.1.0
```

## Input columns
Required:
- `description`

Optional:
- `type` (Added/Changed/Fixed/Removed)
- `ticket`
- `owner`
