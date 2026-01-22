# Demo 3/4 — CD: Deploy to EKS from Jenkins

## Jenkins needs
- docker installed (to build/push images)
- aws cli + kubectl installed
- AWS creds stored in Jenkins credentials
- access to EKS via `aws eks update-kubeconfig`

## Pipelines provided
- jenkins/Jenkinsfile.dockerhub  (private DockerHub -> EKS)
- jenkins/Jenkinsfile.ecr        (AWS ECR -> EKS)

## Deployment approach
Pipelines update the image tag and run:
kubectl apply -k k8s
kubectl -n myapp rollout status deploy/myapp
