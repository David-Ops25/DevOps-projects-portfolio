# Commands Used

> Add your real command history here. The blocks below are safe templates.

## Create EKS with eksctl
```bash
eksctl create cluster -f eksctl/cluster.yaml
```

## Update kubeconfig
```bash
aws eks update-kubeconfig --region us-east-1 --name demo-eks
kubectl get nodes
```

## Deploy sample app
```bash
kubectl apply -f k8s/deploy.yaml
kubectl get svc
```

## Fargate profile (example)
```bash
eksctl create fargateprofile --cluster demo-eks --name fp-default --namespace default
```
