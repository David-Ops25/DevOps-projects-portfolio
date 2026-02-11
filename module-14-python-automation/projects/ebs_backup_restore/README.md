# Project — EBS Backup & Restore

**Goal:** Create tagged EBS snapshots, clean up old snapshots, and restore a volume from the latest snapshot.

## Run
```bash
export AWS_REGION=us-east-1
python3 src/ebs_backup_restore/app.py snapshot --dry-run
python3 src/ebs_backup_restore/app.py cleanup --older-than-days 7 --dry-run
python3 src/ebs_backup_restore/app.py restore --az us-east-1a
```
