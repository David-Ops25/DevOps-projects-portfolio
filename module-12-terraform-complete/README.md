# Module 12 — Infrastructure as Code with Terraform (AWS + EKS)

This repository is a **complete Module 12 project** based on the **TechWorld with Nana DevOps Bootcamp** “Infrastructure as Code with Terraform”.
It includes **all Module 12 demos** as separate, runnable examples:

1. **Automate AWS Infrastructure** (VPC, subnets, routing, SG, EC2) and **deploy a Dockerized app** on the provisioned EC2 instance.  
2. **Modularize Terraform code** into reusable modules (VPC, EC2).  
3. **Provision AWS EKS with Terraform** (cluster + managed node group).  
4. **Complete CI/CD with Terraform** (Jenkins pipeline provisions EC2 with Terraform and deploys with Docker Compose).  
5. **Configure Shared Remote State** using **S3 + DynamoDB state locking**.

These map directly to the Module 12 demo list in the Bootcamp “Demo Projects Overview” (Module 12 section). fileciteturn2file0

## Why this matters in a real DevOps job

IaC solves common work problems:
- manual console setup, inconsistent environments
- infrastructure drift and hard-to-audit changes
- slow provisioning and risky deployments

With Terraform, infrastructure becomes **version-controlled, repeatable, reviewable, and automatable**.

## Repo layout

```
module-12-terraform-complete/
├── examples/
│   ├── 01-aws-infra-ec2-docker/
│   ├── 02-modularized-aws-infra/
│   ├── 03-eks-cluster/
│   ├── 04-cicd-jenkins-terraform/
│   └── 05-remote-state/
├── modules/
│   ├── vpc/
│   ├── ec2/
│   └── eks/
└── docs/
```

## Prerequisites
- AWS account + AWS CLI configured
- Terraform >= 1.6
- (EKS demo) kubectl

## Quickstart
See each demo folder under `examples/` for step-by-step commands.

## Author
Your Name — DevOps / Cloud Engineering Portfolio
