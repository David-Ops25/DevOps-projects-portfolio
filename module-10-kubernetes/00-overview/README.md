# Module 10 Overview — Kubernetes in Practice

This module focuses on practical Kubernetes skills used daily in DevOps/SRE roles:
- Deploying applications with **Deployments/Services**
- Managing configuration with **ConfigMaps** and secrets with **Secrets**
- Running stateful workloads (MongoDB) using **Helm** and **persistent storage**
- Pulling images from a **private container registry** (AWS ECR) using `imagePullSecrets`
- Packaging and reusing K8s manifests with **Helm charts**
- Managing multiple Helm releases consistently with **Helmfile**

## What you’ll find in this repo

Each demo has:
- a `README.md` with step-by-step instructions
- Kubernetes manifests (`.yaml`) and/or Helm/Helmfile configs
- verification commands (how to prove it worked)
- cleanup commands

## Recommended order

Follow the folder order:
1. `01-demo-mongo-minikube/`
2. `02-demo-mongodb-helm-stateful/`
3. `03-demo-mosquitto-config-secret-volumes/`
4. `04-demo-private-registry-aws-ecr/`
5. `05-demo-microservices-best-practices/`
6. `06-demo-helm-chart-microservices/`
7. `07-demo-helmfile/`

## Real DevOps relevance

These demos map directly to common responsibilities:
- **Release engineering:** packaging deployments with Helm, promoting versions across environments
- **Security:** least privilege, secrets handling, image pull auth, non-root containers
- **Reliability:** readiness/liveness probes, replica scaling, controlled rollouts
- **Operations:** debugging pods, observing rollout state, safe cleanup and repeatability
