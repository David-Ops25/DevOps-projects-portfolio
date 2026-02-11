# Module 14 — Python Automation on AWS (Portfolio)

This module demonstrates **production-style AWS automation** using Python, with a focus on:
- **Operational monitoring**
- **Safe remediation / recovery**
- **Tag governance**
- **Backup + restore**
- **Cost hygiene and clean teardown**

It is structured like Module 13 (monorepo with `projects/`, `docs/`, `tests/`).

---

## Quick Start

### 1) Create & activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 2) AWS credentials
This module assumes credentials are available via one of:
- `~/.aws/credentials` (recommended)
- environment variables (`AWS_ACCESS_KEY_ID`, etc.)
- an assumed role via SSO/STS

Set the region explicitly when running demos (avoid accidental region mismatch):
```bash
export AWS_REGION=us-east-1
```

---

## Projects (Demos)

### 1) EC2 Health Checks
Folder: `projects/ec2_health_checks/`

- Verify identity (`sts:GetCallerIdentity`)
- Print EC2 instance + system status checks
- Optional loop mode with interval

### 2) EC2 Auto Tagging
Folder: `projects/ec2_auto_tagging/`

- Apply standard tags safely
- `--dry-run` support
- Filter only running instances

### 3) EKS Cluster Inspection
Folder: `projects/eks_inspection/`

- List clusters
- Describe cluster status, version, networking

### 4) EBS Backup & Restore
Folder: `projects/ebs_backup_restore/`

- Create snapshots (tagged)
- Cleanup old snapshots
- Restore a new volume from latest snapshot

### 5) Website Monitoring + Auto-Recovery
Folder: `projects/website_monitor_recovery/`

- HTTP health check
- If down: SSH in and run recovery command (e.g., restart nginx)
- Recheck and report `RECOVERED`

---

## What I Did (Real Work Summary)

- Built multiple boto3 automation utilities for EC2/EKS/EBS.
- Implemented safe patterns: dry-run, explicit region selection, clear logs.
- Diagnosed real-world issues:
  - Region mismatch (default `eu-north-1` vs resources in `us-east-1`)
  - SSH access loss and recovery using **EC2 Instance Connect**
  - Instances re-created automatically due to **EKS managed nodegroup/ASG**
  - EKS deletion blocked by attached nodegroups (fixed by deleting nodegroup first)
- Performed full cost hygiene teardown:
  - Terminated instances, deleted snapshots, deleted unattached volumes
  - Deleted EKS nodegroup then cluster

---

## Documentation
- Commands used: `docs/COMMANDS_USED.md`
- Challenges + solutions: `docs/CHALLENGES_AND_SOLUTIONS.md`

---

## License
MIT (see repository root license if you use one in the parent portfolio repo).
