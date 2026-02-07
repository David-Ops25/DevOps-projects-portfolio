# Demo 4 — Complete CI/CD with Terraform (Jenkins)

Maps to Module 12 demo: Complete CI/CD with Terraform. fileciteturn2file0

This example includes:
- A Jenkinsfile showing how to run Terraform `init/plan/apply`
- Output the provisioned `public_ip`
- Deploy a docker-compose file over SSH and start the service

Files:
- `Jenkinsfile`
- `terraform/` (Terraform project that provisions EC2 using reusable modules)
