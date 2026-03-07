# Project — EC2 Health Checks

**Goal:** Verify AWS identity and monitor EC2 instance + system status checks.

## Run
```bash
export AWS_REGION=us-east-1
python3 src/ec2_health_checks/app.py whoami
python3 src/ec2_health_checks/app.py status
python3 src/ec2_health_checks/app.py loop --interval 10
```
