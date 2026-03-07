# Demo 2 — Install MongoDB on Kubernetes using Helm (Stateful)

**From the Module 10 overview**: install a stateful service (MongoDB) using Helm, configure persistence, and validate the workload. fileciteturn4file0

This demo uses the widely adopted **Bitnami MongoDB Helm chart** as a practical, production-aligned example.

> If your course used a different chart, the concepts are the same:
> - Helm install/upgrade
> - StatefulSet + PersistentVolumeClaim
> - Parameterization via `values.yaml`
> - Verification and cleanup

---

## Prerequisites

- `kubectl` configured for your cluster (Minikube is fine)
- `helm` installed
- A default StorageClass in the cluster (Minikube usually provides one)

Check:
```bash
kubectl get nodes
kubectl get storageclass
helm version
```

---

## Step-by-step

### 1) Create a namespace
```bash
kubectl create namespace mongodb-helm
```

### 2) Add the Bitnami repo (one-time)
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### 3) Install MongoDB with persistence
This demo installs a **replica set** (replicated MongoDB) with a small persistent volume for each pod.

```bash
helm upgrade --install mongodb bitnami/mongodb   -n mongodb-helm   -f values.yaml
```

### 4) Verify resources
```bash
kubectl -n mongodb-helm get sts,pvc,svc,pods
kubectl -n mongodb-helm rollout status statefulset/mongodb --timeout=300s
```

### 5) Retrieve the root password (demo/learning convenience)
```bash
kubectl -n mongodb-helm get secret mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 -d
echo
```

### 6) (Optional) Port-forward for local testing
```bash
kubectl -n mongodb-helm port-forward svc/mongodb 27017:27017
```

---

## How this is used in real DevOps work

- Stateful workloads (databases, queues) often run as **StatefulSets** with PVCs.
- Helm is the standard delivery mechanism for vendor and platform charts (Bitnami, Prometheus, ingress controllers).
- Values files let you:
  - set replica counts per environment
  - enable/disable persistence
  - control resource requests/limits
  - configure auth and TLS

---

## Cleanup

```bash
helm -n mongodb-helm uninstall mongodb
kubectl delete namespace mongodb-helm
```
