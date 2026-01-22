# Troubleshooting

## kubeconfig issues
aws eks update-kubeconfig --region eu-north-1 --name <CLUSTER_NAME>
kubectl cluster-info

## ImagePullBackOff
- DockerHub: ensure regcred exists in namespace and deployment references it
- ECR: ensure node IAM role can pull, or create secret if required

## Fargate Pending
Ensure Fargate profile selector matches namespace (and labels if used).
