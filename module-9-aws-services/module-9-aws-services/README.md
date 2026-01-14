# Module 9 – AWS Services | End‑to‑End CI/CD Deployment on AWS (Jenkins + Docker)

## What this project is
A recruiter‑friendly, production‑style DevOps portfolio project that implements a complete **CI/CD pipeline** to deploy a containerized application to **AWS EC2** using **Jenkins**, **Docker**, **Docker Compose**, **Docker Hub**, and **AWS CLI**.

This Module 9 project ties together the skills from Modules 5–8 (cloud fundamentals, artifact registries, containerization, CI/CD) into a practical deployment workflow.

## What the project achieves
- Provision and operate EC2 infrastructure for Jenkins (CI) and an application server (CD).
- Build and version Docker images in Jenkins.
- Push images to Docker Hub (or ECR in later enhancements).
- Deploy to an EC2 app server using Docker Compose over SSH.
- Validate deployments with smoke tests.
- Integrate AWS CLI inside Jenkins with credential binding (no hardcoding).

## Skills demonstrated (what recruiters look for)
- AWS: EC2, IAM, security groups, SSH access
- Jenkins: pipelines, credentials, plugins, Dockerized Jenkins
- Containers: Docker build/push, Compose deployments
- Automation: repeatable runbooks, troubleshooting, validation
- Security hygiene: SSH key separation, credential binding, least‑privilege direction

## Quick navigation
- **Architecture:** `architecture/architecture.md`
- **Runbook (step-by-step commands):** `runbook/module-9-runbook.md`
- **Pipelines:** `pipelines/`
- **Docker assets:** `docker/`
- **Troubleshooting + lessons learned:** `challenges-and-lessons.md`
- **Real-world impact:** `real-world-impact.md`

## Deliverables included in this repo folder
- Complete Jenkinsfile templates (CI/CD + deploy)
- Complete Dockerfile and docker-compose.yml templates
- Full command history / syntax to reproduce the environment
- Professional write-up of challenges encountered and solutions
