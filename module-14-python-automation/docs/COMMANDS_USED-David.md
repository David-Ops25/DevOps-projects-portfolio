# Commands Used — Module 14

This document captures the **actual command patterns** used while building and validating the demos.

> Tip: Always pass `--region us-east-1` (or export `AWS_REGION`) to avoid accidental region mismatch.

---

## Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export AWS_REGION=us-east-1
```

---

## Demo 1 — EC2 Health Checks

```bash
python3 projects/ec2_health_checks/src/ec2_health_checks/app.py whoami
python3 projects/ec2_health_checks/src/ec2_health_checks/app.py status
python3 projects/ec2_health_checks/src/ec2_health_checks/app.py loop --interval 10
```

---

## Demo 2 — EC2 Auto Tagging

Dry run first:
```bash
python3 projects/ec2_auto_tagging/src/ec2_auto_tagging/app.py \
  --only-running \
  --tags Environment=dev Owner=david \
  --dry-run
```

Apply for real:
```bash
python3 projects/ec2_auto_tagging/src/ec2_auto_tagging/app.py \
  --only-running \
  --tags Environment=dev Owner=david
```

Verify tags:
```bash
aws ec2 describe-instances --region us-east-1 \
  --filters Name=instance-state-name,Values=running \
  --query "Reservations[].Instances[].{Id:InstanceId,Tags:Tags}" \
  --output json
```

---

## Demo 3 — EKS Cluster Info

```bash
python3 projects/eks_inspection/src/eks_inspection/app.py
```

---

## Demo 4 — EBS Backup & Restore

Create snapshots (dry-run):
```bash
python3 projects/ebs_backup_restore/src/ebs_backup_restore/app.py snapshot --dry-run
```

Cleanup old snapshots (dry-run):
```bash
python3 projects/ebs_backup_restore/src/ebs_backup_restore/app.py cleanup --older-than-days 1 --dry-run
```

Restore a volume from latest snapshot:
```bash
python3 projects/ebs_backup_restore/src/ebs_backup_restore/app.py restore --az us-east-1a
```

---

## Demo 5 — Website Monitoring + Recovery

Monitor only:
```bash
python3 projects/website_monitor_recovery/src/website_monitor_recovery/monitor.py \
  --url http://<PUBLIC_IP>/ --retries 3 --sleep 2
```

Monitor + recover:
```bash
python3 projects/website_monitor_recovery/src/website_monitor_recovery/recover.py \
  --url http://<PUBLIC_IP>/ \
  --ssh-host <PUBLIC_IP> \
  --ssh-user ec2-user \
  --ssh-key /path/to/key.pem \
  --restart-cmd "sudo systemctl restart nginx" \
  --recheck-wait 3
```

---

## SSH Troubleshooting (EC2 Instance Connect)

Get AZ:
```bash
aws ec2 describe-instances --region us-east-1 --instance-ids <INSTANCE_ID> \
  --query "Reservations[0].Instances[0].Placement.AvailabilityZone" --output text
```

Send temporary public key:
```bash
PUBKEY=$(ssh-keygen -y -f /path/to/key.pem)
aws ec2-instance-connect send-ssh-public-key \
  --region us-east-1 \
  --instance-id <INSTANCE_ID> \
  --availability-zone <AZ> \
  --instance-os-user ec2-user \
  --ssh-public-key "$PUBKEY"
```

---

## Cleanup & Cost Hygiene

Running instances:
```bash
aws ec2 describe-instances --region us-east-1 \
  --filters Name=instance-state-name,Values=running \
  --query "Reservations[].Instances[].{Id:InstanceId,Type:InstanceType,Name:Tags[?Key=='Name']|[0].Value}" \
  --output table
```

Terminate:
```bash
aws ec2 terminate-instances --region us-east-1 --instance-ids <ID1> <ID2>
aws ec2 wait instance-terminated --region us-east-1 --instance-ids <ID1> <ID2>
```

Volumes (delete `available`):
```bash
aws ec2 describe-volumes --region us-east-1 \
  --query "Volumes[].{VolumeId:VolumeId,State:State,Size:Size,AttachedTo:Attachments[0].InstanceId}" \
  --output table
aws ec2 delete-volume --region us-east-1 --volume-id <VOLUME_ID>
```

Snapshots:
```bash
aws ec2 describe-snapshots --owner-ids self --region us-east-1 --output table
aws ec2 delete-snapshot --region us-east-1 --snapshot-id <SNAPSHOT_ID>
```

EKS nodegroup + cluster deletion:
```bash
aws eks list-nodegroups --region us-east-1 --cluster-name module12-eks
aws eks delete-nodegroup --region us-east-1 --cluster-name module12-eks --nodegroup-name <NODEGROUP>
aws eks wait nodegroup-deleted --region us-east-1 --cluster-name module12-eks --nodegroup-name <NODEGROUP>
aws eks delete-cluster --region us-east-1 --name module12-eks
aws eks wait cluster-deleted --region us-east-1 --name module12-eks
```

Auto Scaling (debug “instances keep coming back”):
```bash
aws autoscaling describe-auto-scaling-groups --region us-east-1 --output table
```
