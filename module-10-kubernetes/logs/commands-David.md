# Commands Used

> Add your real command history here. The blocks below are safe templates.

## Minikube setup
```bash
minikube start --cpus=4 --memory=8192
kubectl get nodes
```

## Deploy Mongo + Mongo Express
```bash
kubectl apply -f manifests/mongo/
kubectl get pods
minikube service mongo-express
```

## Helm install (managed cluster)
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install mongodb bitnami/mongodb -n data --create-namespace
```

## Helmfile
```bash
helmfile apply
```
