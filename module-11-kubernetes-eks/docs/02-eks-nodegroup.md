# Demo 1 — EKS with Node Group (Managed Worker Nodes)

## Create cluster
eksctl create cluster -f eksctl/cluster-nodegroup.yaml

## Configure kubectl access
aws eks update-kubeconfig --region eu-north-1 --name myapp-eks

## Verify
kubectl get nodes -o wide
kubectl get pods -A

## Deploy sample app
kubectl apply -k k8s
kubectl -n myapp get pods,svc
