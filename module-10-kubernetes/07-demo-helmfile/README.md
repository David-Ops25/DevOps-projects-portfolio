# Demo 7 — Deploy Microservices with Helmfile

## Goal
Use **Helmfile** to manage Helm releases consistently (upgrade, diff, and apply changes).

This demo uses the shared chart from Demo 6.

## Prerequisites
- `helm` installed
- `helmfile` installed
- Helm diff plugin installed:
  ```bash
  helm plugin install https://github.com/databus23/helm-diff
  ```

## Steps

### 1) Create namespace
```bash
kubectl create namespace micro
```

### 2) Apply with Helmfile
```bash
cd 07-demo-helmfile
helmfile -n micro apply
```

### 3) Verify
```bash
kubectl -n micro get deploy,svc,pods
helm -n micro list
```

### 4) Demonstrate an upgrade
Edit `../06-demo-helm-chart-microservices/microservices/values.yaml` (e.g., set `services.frontend.replicaCount: 2`), then:
```bash
helmfile -n micro apply
kubectl -n micro get deploy microservices-frontend
```

## Cleanup
```bash
helm -n micro uninstall microshop
kubectl delete namespace micro
```

## Real DevOps notes
- Helmfile is helpful in repos that deploy multiple Helm releases across environments (dev/stage/prod).
- In production, you typically combine Helmfile with CI/CD (GitHub Actions/Jenkins) and secret management.
