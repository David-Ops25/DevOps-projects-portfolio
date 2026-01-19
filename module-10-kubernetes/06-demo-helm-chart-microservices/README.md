# Demo 6 — Create a Shared Helm Chart for Microservices

## Goal
Create **one reusable Helm chart** that can deploy multiple microservices from a single `values.yaml`.

Instead of duplicating YAML for each service, we define:
- a `services:` map in `values.yaml`
- templates that iterate over the map to render a `Deployment` and `Service` per microservice

This is the foundational pattern for packaging microservices for multiple environments.

## Files
- `microservices/Chart.yaml`
- `microservices/values.yaml`
- `microservices/templates/deployments.yaml`
- `microservices/templates/services.yaml`

## Step-by-step

### 1) Lint and render
```bash
cd microservices
helm lint .
helm template microshop .
```

### 2) Install into Kubernetes
```bash
kubectl create namespace micro
helm install microshop . -n micro
kubectl -n micro get deploy,svc,pods
```

### 3) Upgrade example
Scale `frontend.replicaCount` to 2 and upgrade:
```bash
helm upgrade microshop . -n micro
kubectl -n micro get deploy microservices-frontend
```

## Cleanup
```bash
helm uninstall microshop -n micro
kubectl delete namespace micro
```

## Real DevOps notes
- Helm charts are commonly used for release packaging and environment-specific deployments.
- In production, `values.yaml` is usually split per environment (dev/stage/prod) and combined via GitOps.
