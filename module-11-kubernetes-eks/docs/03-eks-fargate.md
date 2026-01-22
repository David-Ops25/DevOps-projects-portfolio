# Demo 2 — EKS with Fargate Profile

## Create cluster
eksctl create cluster -f eksctl/cluster-fargate.yaml

## Configure kubectl access
aws eks update-kubeconfig --region eu-north-1 --name myapp-fargate

## Deploy
kubectl apply -k k8s
kubectl -n myapp get pods -o wide

## Note
If pods are Pending, the Fargate profile must match the namespace/labels.
