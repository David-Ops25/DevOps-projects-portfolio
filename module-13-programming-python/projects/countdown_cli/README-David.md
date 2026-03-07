# Countdown CLI

A small but production-style CLI tool that prints time remaining until a deadline.

## What problem it solves
When you're tracking delivery dates, release cutoffs, exams, or milestones, a CLI countdown is useful for:
- quick checks from the terminal
- use inside scripts / cron jobs (JSON output)
- consistent timezone handling

## Features
- ISO deadline parsing (supports `Z`)
- timezone-aware display (`--timezone`)
- machine-readable output (`--json`)
- verbose logging (`--verbose`)

## Install (editable)
From the repo root:
```bash
pip install -e projects/countdown_cli
```

## Examples
```bash
countdown --goal "Demo" --deadline "2026-03-01T12:00:00Z" --timezone "Europe/London"
countdown --goal "Demo" --deadline "2026-03-01T12:00:00Z" --json
```

## Test
```bash
pytest -q projects/countdown_cli/tests
```
