# Project — EC2 Auto Tagging

**Goal:** Apply standard tags to EC2 instances with safe dry-run support.

## Run
```bash
export AWS_REGION=us-east-1
python3 src/ec2_auto_tagging/app.py --only-running --tags Environment=dev Owner=david --dry-run
python3 src/ec2_auto_tagging/app.py --only-running --tags Environment=dev Owner=david
```
