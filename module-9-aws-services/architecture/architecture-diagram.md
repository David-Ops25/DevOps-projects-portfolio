# Architecture Overview

## Components
- Developer workstation (Git, AWS CLI)
- GitHub repository (source control)
- Jenkins server (Docker container on EC2)
- Application server (EC2)
- Docker Hub (container registry)

## Flow
1. Code pushed to GitHub
2. Jenkins pipeline triggered
3. Application built into Docker image
4. Image pushed to Docker Hub
5. Jenkins deploys image to EC2 via Docker Compose
6. Smoke tests validate deployment

## Why This Architecture
This mirrors many real-world small-to-mid scale production environments before Kubernetes adoption.