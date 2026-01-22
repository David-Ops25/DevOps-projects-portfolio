# Module 11 – Kubernetes on AWS (EKS)

# Module 11 – Kubernetes on AWS (EKS)

This module demonstrates how to run and deploy containerized applications on a **production-grade, managed Kubernetes platform** using **Amazon Elastic Kubernetes Service (EKS)**.

It builds directly on **Module 10 (Kubernetes)** by moving workloads from local and self-managed clusters into **AWS-managed Kubernetes**, and by integrating Kubernetes deployments into a **CI/CD pipeline**.

---

## 🚀 What This Module Covers

- Provisioning Kubernetes clusters on AWS using **Amazon EKS**
- Comparing **Managed Node Groups vs AWS Fargate**
- Automating cluster creation and lifecycle management with **eksctl**
- Deploying applications to EKS using Kubernetes manifests
- Implementing **Continuous Deployment to EKS from Jenkins**
- Deploying from **private container registries**:
  - Private Docker Hub
  - AWS Elastic Container Registry (ECR)

---

## 🛠️ Technologies Used

- Kubernetes
- AWS EKS
- AWS Fargate
- eksctl
- Jenkins
- Docker
- AWS ECR
- AWS CLI & kubectl
- Linux

---

## 🔗 Relation to Module 10 (Kubernetes)

Module 10 introduced core Kubernetes concepts such as Deployments, Services, ConfigMaps, Secrets, Helm, and microservices.

Module 11 applies those concepts in a **real AWS cloud environment**, adding:
- Cloud-native security (IAM)
- Managed Kubernetes operations
- CI/CD-driven deployments to Kubernetes

Together, Modules 10 and 11 demonstrate:
**Kubernetes fundamentals → Managed Kubernetes → Production CI/CD on AWS**

---

## 📂 Repository Structure

```text
module-11-kubernetes-eks/
├── docs/        # Step-by-step guides and explanations
├── eksctl/      # EKS cluster configurations (NodeGroup & Fargate)
├── k8s/         # Kubernetes manifests (deployment, service, namespace)
├── docker/      # Dockerfiles used for builds
├── jenkins/     # Jenkins pipelines for CD to EKS
└── scripts/     # Helper scripts (cluster creation, cleanup, etc.)

