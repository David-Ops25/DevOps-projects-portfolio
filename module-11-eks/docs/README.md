# EKS + Jenkins CD

## What this project is about
Provision and operate Kubernetes on AWS using EKS, including managed node groups, Fargate profiles, eksctl-based cluster creation, and Jenkins-based deployments to Kubernetes.

## What was done (implementation summary)
- Created EKS cluster + node group
- Created optional Fargate profile
- Created cluster using eksctl (alternative)
- Configured Jenkins with kubectl + kubeconfig
- Deployed manifests from pipeline
- Built end-to-end CI/CD: build → push image → deploy to EKS

## Challenges faced & fixes
- kubectl auth errors → fixed IAM mapping and kubeconfig
- LoadBalancer pending → ensured subnets tagged and controller installed if needed
- Image pulls failed → configured imagePullSecrets for private registries

## Files in this folder
See: [`files.md`](../docs/files.md)

## Commands used
See: [`../logs/commands.md`](../logs/commands.md)

## Next improvements (optional)
- Use GitOps (ArgoCD)
- Add namespace RBAC
- Add monitoring stack (Prometheus/Grafana)
