# Architecture

## Components
1. **Developer workstation**
   - Used to generate SSH keys, configure AWS CLI, and manage GitHub.
2. **GitHub repository**
   - Stores application code + Jenkins pipeline definition (Jenkinsfile) + runbooks.
3. **Jenkins Server (EC2)**
   - Jenkins runs **inside a Docker container** on an EC2 instance.
   - Jenkins builds images and orchestrates deployments.
4. **Application Server (EC2)**
   - Runs Docker + Docker Compose.
   - Hosts the running application and supporting services (MongoDB + Mongo Express).
5. **Container Registry**
   - Docker Hub (primary in this project) or ECR (optional extension).

## Data & control flow
1. Developer pushes code to GitHub.
2. Jenkins checks out repo.
3. Jenkins builds a Docker image and tags it with `BUILD_NUMBER`.
4. Jenkins logs in to Docker Hub and pushes the image.
5. Jenkins SSHs into the app server and deploys via Docker Compose.
6. Jenkins runs a smoke test on the app server to verify the deployment.

## Why this mirrors real environments
Many organizations run workloads on EC2 (VMs) and use Jenkins for CI/CD.
This project shows how to deliver consistent deployments without Kubernetes, while still
using strong automation and validation practices.
