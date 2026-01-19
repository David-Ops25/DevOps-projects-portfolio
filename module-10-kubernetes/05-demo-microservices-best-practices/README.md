# Demo 5 — Deploy Microservices Application on Kubernetes (Best Practices)

**Goal (Module 10):** deploy a small microservices-style application and apply best practices:
- consistent labels/selectors
- resource requests/limits
- readiness/liveness probes
- environment configuration via ConfigMaps/Secrets
- clean separation of components (one deployment per service)
- simple service discovery via ClusterIP services

> The course demo may use a specific “microservices shop” app.
> This repo provides a **vendor-neutral reference implementation** that demonstrates the same Kubernetes patterns
> using lightweight public images.

---

## Architecture (demo)

- `frontend` (nginx) — acts as a simple web entrypoint
- `api` (http-echo) — simulates a backend API
- `redis` — simulates a shared backing service

All services are internal (`ClusterIP`). You can port-forward the frontend for testing.

---

## Step-by-step

### 1) Create namespace
```bash
kubectl create namespace microservices
```

### 2) Apply config and secrets
```bash
kubectl -n microservices apply -f configmap.yaml
kubectl -n microservices apply -f secret.yaml
```

### 3) Deploy services
```bash
kubectl -n microservices apply -f redis.yaml
kubectl -n microservices apply -f api.yaml
kubectl -n microservices apply -f frontend.yaml
```

### 4) Verify
```bash
kubectl -n microservices get deploy,svc,pods
kubectl -n microservices rollout status deploy/frontend --timeout=180s
kubectl -n microservices rollout status deploy/api --timeout=180s
kubectl -n microservices rollout status deploy/redis --timeout=180s
```

### 5) Test via port-forward
```bash
kubectl -n microservices port-forward svc/frontend 8080:80
# open http://localhost:8080
```

---

## Best practices checklist (what this demo demonstrates)

- **Labels & selectors:** stable and consistent for services and deployments
- **Probes:** readiness & liveness for safer rollouts
- **Resources:** requests/limits to support scheduling and prevent noisy neighbors
- **Config externalization:** configmaps/secrets allow changing config without rebuilding images
- **Least privilege:** example `securityContext` on pods/containers

---

## Real DevOps implementation notes

In real environments you would extend this with:
- Ingress controller + TLS (cert-manager)
- NetworkPolicies (restrict east-west traffic)
- HPA and/or KEDA for scaling
- PodDisruptionBudgets
- GitOps (Argo CD / Flux)
- External secrets integration (Vault / AWS Secrets Manager)
- Observability (Prometheus + Grafana + Loki)

---

## Cleanup
```bash
kubectl delete namespace microservices
```
