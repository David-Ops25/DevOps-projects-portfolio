# Module 12 — Infrastructure as Code with Terraform (AWS + EKS)

**Author:** David Angyu  
**Email:** angyu84@gmail.com  
**Portfolio Repo:** DevOps-projects-portfolio (Module 12)  

## What this project is
This is my **hands-on Terraform portfolio project** for **Module 12 (Infrastructure as Code with Terraform)** from the *TechWorld with Nana DevOps Bootcamp*.

It contains **runnable examples** that cover the complete Module 12 journey:
1) Provision AWS infrastructure with Terraform (VPC + networking + EC2) and bootstrap the instance to run a Docker workload  
2) Refactor infrastructure into **reusable Terraform modules** (VPC + EC2)  
3) Provision an **AWS EKS** cluster with Terraform (cluster + managed node group)  
4) Show a **CI/CD-ready pattern** where a pipeline can provision infra with Terraform and deploy with Docker Compose  
5) Configure **shared remote state** using **S3 + DynamoDB locking** (team-ready IaC workflow)

> Goal: demonstrate real DevOps infrastructure work (repeatable, reviewable, and automatable), not just theory.

---

## Why this matters in a real work environment
In many teams, infrastructure is still created manually in the AWS Console. That leads to common problems:

- **Inconsistent environments** (dev ≠ staging ≠ prod)  
- **No audit trail** of infrastructure changes  
- **Slow provisioning** (hours/days instead of minutes)  
- **Configuration drift** and fragile deployments  
- Difficult onboarding for new engineers (“tribal knowledge”)

This project addresses those problems by using **Infrastructure as Code**:
- Infrastructure becomes **version-controlled** (Git), reviewable via PRs
- Environments become **repeatable** and easy to recreate
- Changes become safer through **plan → review → apply**
- Team workflows are supported using **remote state + locking**

---

## Repository structure
```
module-12-terraform/
├── README.md
├── Makefile
├── .gitignore
├── docs/
│   ├── ARCHITECTURE.md
│   └── WORK_LOG.md
├── modules/
│   ├── vpc/
│   ├── ec2/
│   └── eks/
└── examples/
    ├── 01-aws-infra-ec2-docker/
    ├── 02-modularized-aws-infra/
    ├── 03-eks-cluster/
    ├── 04-cicd-jenkins-terraform/
    └── 05-remote-state/
```

### How to use the repo
Each folder under `examples/` is a **standalone Terraform root module**.
That means you can run Terraform from inside any example like this:

```bash
cd module-12-terraform/examples/01-aws-infra-ec2-docker
terraform init
terraform plan -var-file=env/dev.tfvars
terraform apply -var-file=env/dev.tfvars
```

---

## What I implemented (high-level)
### Example 01 — AWS Infra + EC2 bootstrap for Docker
- VPC + subnet + route table + IGW
- Security group
- EC2 instance
- `user_data` bootstrap: installs Docker & Docker Compose and starts a containerized workload

### Example 02 — Modularized AWS infrastructure
- Refactored VPC + EC2 into reusable modules under `/modules`
- Cleaner root configuration using module inputs/outputs

### Example 03 — Terraform & AWS EKS
- EKS cluster provisioning using Terraform
- Managed node group creation
- Outputs required to connect using `aws eks update-kubeconfig`

### Example 04 — CI/CD-ready Terraform pattern
- Terraform lives alongside pipeline assets (example Jenkins workflow)
- Shows how a pipeline can provision EC2 using Terraform and deploy with Docker Compose

### Example 05 — Remote state (S3 + DynamoDB)
- Backend example configuration for remote state
- Locking pattern for safe teamwork and avoiding state corruption

---

## Prerequisites
- Terraform (>= 1.6)
- AWS CLI configured (`aws configure`)
- An AWS account with permissions to create VPC/EC2/EKS resources
- (For EKS example) `kubectl`

---

## Safety notes
- This repo is designed for learning/portfolio. **Review the plan** before applying.
- Always destroy resources after testing to avoid unexpected AWS costs:

```bash
terraform destroy -var-file=env/dev.tfvars
```

---

## Evidence of work
See:
- `docs/WORK_LOG.md` for the execution log format and notes
- `docs/ARCHITECTURE.md` for diagrams and reasoning

---

## Next improvements (planned)
- Add GitHub Actions pipeline to validate Terraform formatting and `terraform validate`
- Extend examples with multi-environment structure (dev/stage/prod)
- Deploy a sample app to EKS using Helm and add basic observability

---
