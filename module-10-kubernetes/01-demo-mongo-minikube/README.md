# Demo 1 — MongoDB + Mongo Express on Minikube

## Goal
Deploy MongoDB and Mongo Express into a local Kubernetes cluster (Minikube) and externalize configuration with a **ConfigMap** and credentials with a **Secret**.

## Prerequisites
- Minikube running: `minikube start`
- `kubectl` installed

## Files
- `mongo-configmap.yaml`
- `mongo-secret.yaml`
- `mongodb-deployment.yaml`
- `mongodb-service.yaml`
- `mongo-express-deployment.yaml`
- `mongo-express-service.yaml`

## Step‑by‑step

1) Create a namespace
```bash
kubectl create namespace mongo-demo
```

2) Apply ConfigMap and Secret
```bash
kubectl -n mongo-demo apply -f mongo-configmap.yaml
kubectl -n mongo-demo apply -f mongo-secret.yaml
```

3) Deploy MongoDB
```bash
kubectl -n mongo-demo apply -f mongodb-deployment.yaml
kubectl -n mongo-demo apply -f mongodb-service.yaml
```

4) Deploy Mongo Express
```bash
kubectl -n mongo-demo apply -f mongo-express-deployment.yaml
kubectl -n mongo-demo apply -f mongo-express-service.yaml
```

5) Verify
```bash
kubectl -n mongo-demo get all
kubectl -n mongo-demo get pods -w
```

6) Access Mongo Express (NodePort)
```bash
minikube service mongo-express -n mongo-demo
```

## Troubleshooting
- If Mongo Express shows auth errors, re-check Secret values.
- If pods are Pending, check resources: `kubectl -n mongo-demo describe pod <pod>`.

## Cleanup
```bash
kubectl delete namespace mongo-demo
```

## Real‑world DevOps notes
- Use **Secrets** for passwords and tokens; do not hardcode credentials in manifests.
- In real clusters, use **Ingress** or a Gateway instead of NodePort.
- `mongodb-service.yaml`
- `mongo-express-deployment.yaml`
- `mongo-express-service.yaml`

## Step-by-step

### 1) Create namespace
```bash
kubectl create namespace mongo-demo
```

### 2) Apply ConfigMap and Secret
```bash
kubectl -n mongo-demo apply -f mongo-configmap.yaml
kubectl -n mongo-demo apply -f mongo-secret.yaml
```

### 3) Deploy MongoDB
```bash
kubectl -n mongo-demo apply -f mongodb-deployment.yaml
kubectl -n mongo-demo apply -f mongodb-service.yaml
```

### 4) Deploy Mongo Express
```bash
kubectl -n mongo-demo apply -f mongo-express-deployment.yaml
kubectl -n mongo-demo apply -f mongo-express-service.yaml
```

### 5) Verify
```bash
kubectl -n mongo-demo get all
kubectl -n mongo-demo get pods -w
```

### 6) Access the UI
This pack ships a NodePort example. Get the Minikube URL:
```bash
minikube service -n mongo-demo mongo-express --url
```
Open the printed URL in the browser.

## Cleanup
```bash
kubectl delete namespace mongo-demo
```

## Real DevOps notes
- ConfigMap/Secret separation is standard for 12‑factor style deployments.
- In production you would use **External Secrets** (Vault/AWS Secrets Manager) and **NetworkPolicies**.
