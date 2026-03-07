# Module 16 Commands

All commands below are grouped in the order used during the project.

## 1. AWS CLI setup

```bash
aws configure
aws configure set region eu-north-1
aws configure get region
aws sts get-caller-identity
```

## 2. Create EKS cluster with eksctl

```bash
eksctl create cluster \
  --name monitoring-cluster \
  --region eu-north-1 \
  --nodegroup-name workers \
  --node-type t3.medium \
  --nodes 2
```

Verify cluster:

```bash
kubectl get nodes
kubectl get pods -n kube-system
```

## 3. Install kube-prometheus-stack

```bash
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring
kubectl get pods -n monitoring
```

## 4. Access Grafana and Prometheus

Grafana:

```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
kubectl get secret monitoring-grafana -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 --decode && echo
```

Prometheus:

```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring
```

Alertmanager:

```bash
kubectl port-forward svc/monitoring-kube-prometheus-alertmanager 9093:9093 -n monitoring
```

## 5. Alerting rules

Apply the Prometheus rules file:

```bash
kubectl apply -f k8s/alerts/alerts.yaml
kubectl get prometheusrules -n monitoring
```

## 6. Redis monitoring demo

Create application namespace:

```bash
kubectl create namespace apps
```

Initial Redis install:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install redis bitnami/redis -n apps
```

If Redis is pending because of PVC issues, use non-persistent standalone mode:

```bash
helm uninstall redis -n apps
helm install redis bitnami/redis -n apps \
  --set architecture=standalone \
  --set master.persistence.enabled=false \
  --set master.resources.requests.cpu=100m \
  --set master.resources.requests.memory=128Mi
```

Install Redis exporter:

```bash
helm upgrade --install redis-exporter prometheus-community/prometheus-redis-exporter \
  --namespace apps \
  --set "redisAddress=redis://:YOUR_REDIS_PASSWORD@redis-master.apps.svc.cluster.local:6379"
```

Apply Redis ServiceMonitor:

```bash
kubectl apply -f k8s/monitoring/redis-sm.yaml
kubectl get servicemonitor -A | grep redis
```

Troubleshooting:

```bash
kubectl get pods -n apps
kubectl get svc -n apps
kubectl describe svc redis-exporter-prometheus-redis-exporter -n apps
kubectl logs -n apps deploy/redis-exporter-prometheus-redis-exporter
kubectl port-forward svc/redis-exporter-prometheus-redis-exporter 9121:9121 -n apps
curl -s localhost:9121/metrics | grep redis_up
```

Prometheus query:

```text
redis_up
```

## 7. Own application monitoring demo

Move into the app directory:

```bash
cd apps/node-monitor
npm install
```

Optional local test:

```bash
node app.js
```

Build and push Docker image:

```bash
docker login -u YOUR_DOCKERHUB_USERNAME
docker build -t YOUR_DOCKERHUB_USERNAME/node-monitor:1.0 .
docker push YOUR_DOCKERHUB_USERNAME/node-monitor:1.0
```

Deploy the app and ServiceMonitor:

```bash
kubectl apply -f k8s/apps/node-app.yaml
kubectl apply -f k8s/apps/node-sm.yaml
kubectl get pods -n apps
kubectl get svc -n apps
```

Generate traffic to the app:

```bash
kubectl port-forward svc/node-app 3001:3000 -n apps
```

Prometheus query:

```text
app_http_requests_total
```

## 8. Cleanup

Delete the EKS cluster:

```bash
eksctl delete cluster --name monitoring-cluster --region eu-north-1
```

## 9. Verify no costly AWS resources remain

Stockholm region:

```bash
aws eks list-clusters --region eu-north-1
aws ec2 describe-instances --region eu-north-1 --query 'Reservations[].Instances[?State.Name==`running`].[InstanceId,InstanceType]'
aws ec2 describe-volumes --region eu-north-1 --query 'Volumes[?State==`available`].[VolumeId,Size]'
aws elbv2 describe-load-balancers --region eu-north-1 --query 'LoadBalancers[].LoadBalancerArn'
aws ec2 describe-addresses --region eu-north-1
aws ec2 describe-nat-gateways --region eu-north-1 --query 'NatGateways[].State'
```

N. Virginia region:

```bash
aws eks list-clusters --region us-east-1
aws ec2 describe-instances --region us-east-1 --query 'Reservations[].Instances[?State.Name==`running`].[InstanceId,InstanceType]'
aws ec2 describe-volumes --region us-east-1 --query 'Volumes[?State==`available`].[VolumeId,Size]'
aws elbv2 describe-load-balancers --region us-east-1 --query 'LoadBalancers[].LoadBalancerArn'
aws ec2 describe-addresses --region us-east-1
aws ec2 describe-nat-gateways --region us-east-1 --query 'NatGateways[].State'
```

If a NAT Gateway remains:

```bash
aws ec2 delete-nat-gateway --region us-east-1 --nat-gateway-id NAT_GATEWAY_ID
```

If an Elastic IP remains unattached:

```bash
aws ec2 release-address --region us-east-1 --allocation-id EIP_ALLOCATION_ID
```
