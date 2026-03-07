# Challenges Faced and How They Were Solved

## 1. EKS addon warning during cluster creation

### Problem
During cluster creation, `eksctl` displayed a warning about recommended policies for the `vpc-cni` addon and mentioned that OIDC was disabled.

### Why it happened
The cluster was created without OIDC, so `eksctl` could not automatically wire IAM permissions for the addon through the older IRSA path.

### How it was solved
The cluster still completed successfully, worker nodes became `Ready`, and Module 16 work could continue. Since there was no active networking failure, the warning was treated as informational for this lab.

### Lesson learned
Not every warning is a blocker. Always verify cluster health with:

```bash
kubectl get nodes
kubectl get pods -n kube-system
```

---

## 2. Prometheus port-forward conflict

### Problem
Port-forwarding Prometheus failed with `address already in use` on port `9090`.

### Why it happened
A previous local process was already using the same port.

### How it was solved
Either the existing port-forward session was reused, or a different local port was used temporarily.

Example:

```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9091:9090 -n monitoring
```

### Lesson learned
The format is `LOCAL_PORT:REMOTE_PORT`. Local port conflicts are common during labs.

---

## 3. Redis pods stuck in Pending

### Problem
Redis pods were created but stayed in `Pending` state.

### Why it happened
The initial Redis Helm chart installation requested persistent storage through PVCs, but the cluster did not have a working dynamic volume provisioning path for this setup.

`kubectl describe pod` showed:

```text
pod has unbound immediate PersistentVolumeClaims
```

### How it was solved
Redis was reinstalled in standalone mode without persistence.

```bash
helm uninstall redis -n apps
helm install redis bitnami/redis -n apps \
  --set architecture=standalone \
  --set master.persistence.enabled=false \
  --set master.resources.requests.cpu=100m \
  --set master.resources.requests.memory=128Mi
```

### Lesson learned
For a monitoring lab, persistence is not always necessary. Reduce complexity when the module goal is observability, not stateful storage design.

---

## 4. Prometheus showed no Redis metrics

### Problem
The `redis_up` query in Prometheus returned an empty result.

### Why it happened
There were multiple configuration mismatches before the final working setup:

- the `ServiceMonitor` was first created in the wrong namespace
- the endpoint port name in the `ServiceMonitor` did not match the exporter service
- the exporter itself could not authenticate to Redis

### How it was solved
Three fixes were applied:

#### a) Move `ServiceMonitor` to the `monitoring` namespace
Prometheus was discovering `ServiceMonitor` objects from the monitoring namespace.

#### b) Fix the endpoint port name
The service exposed port name:

```text
redis-exporter
```

So the `ServiceMonitor` was changed from:

```yaml
- port: metrics
```

to:

```yaml
- port: redis-exporter
```

#### c) Pass the correct Redis password to the exporter
The exporter originally logged:

```text
NOAUTH Authentication required.
```

It was reconfigured using the Redis password stored in the Kubernetes secret.

```bash
REDIS_PASSWORD=$(kubectl get secret redis -n apps -o jsonpath="{.data.redis-password}" | base64 --decode)

helm upgrade --install redis-exporter prometheus-community/prometheus-redis-exporter \
  --namespace apps \
  --set "redisAddress=redis://:${REDIS_PASSWORD}@redis-master.apps.svc.cluster.local:6379"
```

### Validation
Exporter test:

```bash
kubectl port-forward svc/redis-exporter-prometheus-redis-exporter 9121:9121 -n apps
curl -s localhost:9121/metrics | grep redis_up
```

Expected output:

```text
redis_up 1
```

### Lesson learned
When metrics are missing, validate the whole chain:

1. workload is running
2. exporter is running
3. service exists
4. `ServiceMonitor` namespace and labels are correct
5. endpoint port names match
6. exporter can authenticate to the backend service

---

## 5. Docker login confusion during image push

### Problem
Docker CLI defaulted to web-based login, and the initial login flow was interrupted.

### Why it happened
The CLI was started without the username flag, and the browser flow was cancelled.

### How it was solved
Docker login was completed using the correct Docker Hub username.

```bash
docker login -u YOUR_DOCKERHUB_USERNAME
```

Then the image was built and pushed with the correct tag.

```bash
docker build -t YOUR_DOCKERHUB_USERNAME/node-monitor:1.0 .
docker push YOUR_DOCKERHUB_USERNAME/node-monitor:1.0
```

### Lesson learned
Image tags must match the actual Docker Hub account name used for authentication.

---

## 6. Validating the custom Node.js metric

### Problem
The app had to expose custom Prometheus metrics and prove they were being scraped successfully.

### How it was solved
The Node.js app was built with `prom-client`, deployed to EKS, exposed through a Kubernetes service, and scraped by Prometheus through a `ServiceMonitor`.

Prometheus query used:

```text
app_http_requests_total
```

Traffic was generated with:

```bash
kubectl port-forward svc/node-app 3001:3000 -n apps
```

Then the app root URL was refreshed several times to increase the counter.

### Lesson learned
Counters only increase when the application endpoint is actually called. Empty results often just mean no traffic has hit the instrumented route yet.

---

## 7. AWS cleanup and cost control

### Problem
After deleting the EKS cluster, leftover AWS resources still existed in another region.

### Why it happened
Cloud labs often leave resources in multiple regions. In this case, `us-east-1` still had an old NAT Gateway and Elastic IP from an earlier module.

### How it was solved
A region-by-region audit was run using AWS CLI for:

- EKS clusters
- EC2 instances
- EBS volumes
- Elastic IPs
- Load balancers
- NAT Gateways

The remaining NAT Gateway was deleted first, then the Elastic IP was verified as gone.

### Lesson learned
Always verify cleanup in every region you used, not just the current one. NAT Gateways and unattached EBS volumes are frequent hidden costs.
