# Demo 3 — Deploy Mosquitto with ConfigMap & Secret Volumes

**Goal (Module 10):** demonstrate configuration and credentials injected via **volumes** (not env vars). fileciteturn4file0

Mosquitto is a lightweight MQTT broker that uses file-based configuration, making it ideal for practicing:
- ConfigMap mounted as a config file
- Secret mounted as a password file
- Deployments + Services

---

## Prerequisites

- `kubectl` access to a cluster (Minikube works)
- Basic understanding of ConfigMaps and Secrets

---

## Step-by-step

### 1) Create a namespace
```bash
kubectl create namespace mosquitto
```

### 2) Apply ConfigMap and Secret
```bash
kubectl -n mosquitto apply -f mosquitto-configmap.yaml
kubectl -n mosquitto apply -f mosquitto-secret.yaml
```

### 3) Deploy Mosquitto + Service
```bash
kubectl -n mosquitto apply -f mosquitto-deployment.yaml
kubectl -n mosquitto apply -f mosquitto-service.yaml
```

### 4) Verify
```bash
kubectl -n mosquitto get deploy,svc,pods
kubectl -n mosquitto logs deploy/mosquitto --tail=50
```

---

## Why this matters in real DevOps work

Many production components are configured via files, not env vars:
- NGINX / Envoy / HAProxy
- Mosquitto / Kafka configs
- TLS certs, private keys, and auth files

Mounting ConfigMaps/Secrets as volumes enables:
- Separation of code and config
- Safer secret delivery than baking secrets into images
- Standardization across environments

---

## Cleanup

```bash
kubectl delete namespace mosquitto
```
