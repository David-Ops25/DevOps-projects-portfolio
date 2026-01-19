# Module 10 — Container Orchestration with Kubernetes (TWN)

This folder is a **professional, GitHub-ready** documentation pack for **Module 10** of the TechWorld with Nana DevOps Bootcamp.

It documents the full set of Module 10 demos and provides:
- step-by-step instructions for each demo
- Kubernetes manifests (YAML), Helm chart templates, and Helmfile configs
- verification and cleanup commands
- “real DevOps” notes on how these patterns are used in production

> Source reference: the Module 10 demo list and descriptions are taken from `TWN_Demo_Projects_Overview_2.0.pdf`. fileciteturn4file0

---

## Module 10 demos (complete list)

1. **MongoDB + Mongo Express on Minikube** (ConfigMap + Secret)
2. **MongoDB using Helm** (stateful install; persistence)
3. **Mosquitto** (ConfigMap and Secret mounted as volumes)
4. **Deploy web app from a private Docker registry** (AWS ECR + `imagePullSecrets`)
5. **Deploy microservices application with best practices** (probes, resources, clean labels, config)
6. **Create 1 shared Helm chart for microservices** (reusable templates)
7. **Deploy microservices with Helmfile** (consistent multi-release management)

---

## Repository structure

```text
module-10-kubernetes/
  00-overview/
  01-demo-mongo-minikube/
  02-demo-mongodb-helm-stateful/
  03-demo-mosquitto-config-secret-volumes/
  04-demo-private-registry-aws-ecr/
  05-demo-microservices-best-practices/
  06-demo-helm-chart-microservices/
  07-demo-helmfile/
  scripts/
  assets/
```

Each demo folder contains its own `README.md` plus the necessary manifests/configs.

---

## Prerequisites

### Core tools
- `kubectl`
- a Kubernetes cluster (Minikube works for most demos; cloud cluster optional)
- `docker`
- `helm`

### Demo 4 only (AWS ECR)
- AWS account
- `aws` CLI configured (`aws sts get-caller-identity` works)

### Demo 7 (Helmfile)
- `helmfile`
- Helm Diff plugin (`helm plugin install https://github.com/databus23/helm-diff`)

---

## Quick start (recommended)

1) Start / verify your cluster
```bash
minikube start
kubectl get nodes
```

2) Pick a demo folder and follow its README:
- `01-demo-mongo-minikube/README.md`
- `04-demo-private-registry-aws-ecr/README.md`
- `06-demo-helm-chart-microservices/README.md`

---

## What you learn in Module 10 (and why it matters)

### Kubernetes fundamentals used in production
- **Deployments** for stateless workloads and safe rollouts
- **Services** for stable networking and service discovery
- **ConfigMaps** for externalized configuration
- **Secrets** for credentials and sensitive data
- **Volumes & mounts** for file-based config/secrets (common for brokers/proxies)

### Packaging and operating at scale
- **Helm** to templatize and parameterize deployments across environments
- **Helmfile** to manage multiple Helm releases consistently (typical microservices reality)
- **Private registry pulls (ECR)** to support secure supply chains and restricted images

---

## Real DevOps implementation notes

In real teams, these patterns usually evolve into:
- GitOps (Argo CD / Flux) for deployments
- External Secrets (Vault / AWS Secrets Manager / ExternalSecrets Operator)
- Policy (OPA/Gatekeeper/Kyverno) enforcing security and standards
- Observability (Prometheus/Grafana, Loki, OpenTelemetry)
- Controlled rollouts (Argo Rollouts / Flagger), HPA/KEDA for scaling
- NetworkPolicies to reduce blast radius

---

## Cleanup

See `scripts/cleanup-all-minikube.sh` for a quick cleanup helper.

You can also delete demo namespaces individually as shown in each demo README.
