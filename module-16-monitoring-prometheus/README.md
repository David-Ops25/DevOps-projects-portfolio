# Module 16 – Monitoring with Prometheus on AWS EKS

This project is a portfolio-ready implementation of **Module 16 – Monitoring with Prometheus** from the TWN DevOps Bootcamp. It follows the module's recommended toolchain and workflow using **AWS EKS**, **eksctl**, **Helm**, **Prometheus**, **Alertmanager**, **Grafana**, **Redis**, **Docker**, **Node.js**, and **Kubernetes**.

## What this project is about

This module focuses on **observability** in Kubernetes:

- building a managed Kubernetes cluster on **AWS EKS**
- installing a full monitoring stack with **Helm**
- using **Prometheus** to collect cluster and application metrics
- using **Alertmanager** to route alerts
- using **Grafana** to visualize data
- monitoring both a **third-party application (Redis)** and **a custom Node.js application**

## What problem this project solves

In modern deployments, applications can fail silently if there is no visibility into:

- pod health
- CPU and memory usage
- application response behavior
- dependency availability
- infrastructure problems across nodes and services

This project solves that by creating a monitoring platform that:

- detects unhealthy workloads early
- exposes live metrics from Kubernetes and applications
- provides dashboards for operations teams
- prepares the environment for alert-based incident response

## Demos covered

This project covers all four Module 16 demos:

1. **Install Prometheus Stack in Kubernetes** ✅
2. **Configure Alerting for our Application** ✅
3. **Configure Monitoring for a Third-Party Application (Redis)** ✅
4. **Configure Monitoring for Own Application (Node.js)** ✅

## Architecture

```text
AWS EKS Cluster (eu-north-1)
├── monitoring namespace
│   ├── kube-prometheus-stack
│   │   ├── Prometheus
│   │   ├── Alertmanager
│   │   ├── Grafana
│   │   ├── kube-state-metrics
│   │   └── node-exporter
│   └── ServiceMonitors
│       ├── redis-exporter
│       └── node-app
└── apps namespace
    ├── Redis
    ├── Redis Exporter
    └── Node.js app with /metrics endpoint
```

## Repository structure

```text
module-16-monitoring-prometheus/
├─ apps/
│  └─ node-monitor/
│     ├─ app.js
│     ├─ package.json
│     ├─ Dockerfile
│     └─ .dockerignore
├─ docs/
│  ├─ CHALLENGES.md
│  └─ COMMANDS.md
├─ k8s/
│  ├─ alerts/
│  │  └─ alerts.yaml
│  ├─ apps/
│  │  ├─ node-app.yaml
│  │  └─ node-sm.yaml
│  └─ monitoring/
│     └─ redis-sm.yaml
├─ logs/
│  └─ SESSION-NOTES.md
├─ scripts/
│  ├─ create-cluster.sh
│  ├─ install-monitoring-stack.sh
│  ├─ cleanup-cluster.sh
│  └─ aws-cost-check.sh
└─ README.md
```

## Key implementation highlights

### 1) EKS cluster build
- Region: `eu-north-1`
- Cluster name: `monitoring-cluster`
- Worker nodes: `t3.medium`
- Provisioning tool: `eksctl`

### 2) Monitoring stack install
- Helm chart: `prometheus-community/kube-prometheus-stack`
- Namespace: `monitoring`
- Components exposed locally using `kubectl port-forward`

### 3) Alerting
- Custom `PrometheusRule` added for:
  - high CPU usage
  - pods not in running state

### 4) Redis monitoring
- Redis deployed in Kubernetes
- Redis Exporter deployed with password-based connection
- `ServiceMonitor` created in the `monitoring` namespace
- `redis_up` validated in both exporter metrics and Prometheus UI

### 5) Own application monitoring
- Node.js app instrumented using `prom-client`
- Custom metric: `app_http_requests_total`
- App containerized and pushed to Docker Hub
- Deployed to EKS and scraped through a `ServiceMonitor`

## Commands and manifests

See:
- [`docs/COMMANDS.md`](docs/COMMANDS.md)
- [`k8s/`](k8s/)
- [`apps/node-monitor/`](apps/node-monitor/)

## Challenges faced and how they were solved

See [`docs/CHALLENGES.md`](docs/CHALLENGES.md).

Main issues solved during the project:

- EKS addon warning for `vpc-cni`
- port-forward local port conflicts
- Redis pods stuck in `Pending`
- unbound PVCs from persistent Redis install
- ServiceMonitor namespace mismatch
- wrong ServiceMonitor port name
- Redis exporter authentication failure
- AWS cleanup verification to avoid charges

## Security notes

This project intentionally does **not** include:

- AWS access keys
- kubeconfig files
- Redis passwords
- Docker Hub passwords or tokens
- private SSH keys

Use environment variables, AWS CLI credentials, Kubernetes Secrets, and your own secure local configuration.

## Ready-to-push Git commands

From the root of your cloned portfolio repo:

```bash
git checkout -b add-module-16-monitoring
cp -r /path/to/module-16-monitoring-prometheus ./module-16-monitoring-prometheus

git add module-16-monitoring-prometheus

git commit -m "Add Module 16 monitoring project with EKS, Prometheus, Grafana, Redis, and Node.js app"
git push origin add-module-16-monitoring
```

## Suggested root README update

Add this new folder to your repo quick navigation:

- `module-16-monitoring-prometheus/`

And add a link named:

- **Module 16 – Monitoring with Prometheus**

