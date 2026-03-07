# Session Notes

This project was completed interactively on AWS EKS using the following implementation path:

- cluster region: `eu-north-1`
- cluster name: `monitoring-cluster`
- Docker Hub namespace used for the app image: `davidangyu`

## Verified outcomes

- Prometheus stack installed successfully on EKS
- Grafana login validated
- Alertmanager UI validated
- Redis exporter returned:

```text
redis_up 1
```

- Custom Node.js application metric scraped successfully:

```text
app_http_requests_total
```

## Cleanup performed

- EKS cluster deleted in `eu-north-1`
- AWS cost check performed in both `eu-north-1` and `us-east-1`
- old NAT Gateway identified in `us-east-1` and deleted
- Elastic IP verified removed

## Notes for GitHub

Do not commit:

- `.kube/config`
- passwords or tokens
- AWS credentials
- secret values copied from Kubernetes

