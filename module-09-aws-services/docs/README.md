# AWS Deployments + AWS CLI + ECR

## What this project is about
Deploy containerized applications to AWS EC2 manually and automatically from Jenkins, learn AWS CLI automation, and publish images to Amazon ECR.

## What was done (implementation summary)
- Provisioned EC2 and installed Docker
- Deployed app image manually
- Extended Jenkins pipeline to SSH into EC2 and deploy new versions
- Deployed with docker-compose and used remote scripts
- Practiced AWS CLI: EC2, key pairs, IAM resources
- Created ECR repo and pushed images

## Challenges faced & fixes
- SSH auth issues → fixed key permissions and security group inbound
- Docker compose not installed → installed plugin / binary
- ECR auth expired → used `aws ecr get-login-password`

## Files in this folder
See: [`files.md`](../docs/files.md)

## Commands used
See: [`../logs/commands.md`](../logs/commands.md)

## Next improvements (optional)
- Use Terraform (Module 12) instead of manual infra
- Add ALB + HTTPS
- Add monitoring and log shipping
