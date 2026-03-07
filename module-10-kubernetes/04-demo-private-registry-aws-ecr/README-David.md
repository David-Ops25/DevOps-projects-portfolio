# Demo 4 — Deploy a Web App from a Private Docker Registry (AWS ECR)

## Goal
Push a Docker image to **AWS ECR** and deploy it to Kubernetes using an **imagePullSecret**.

This demo proves you can:
- use a private registry securely
- create a K8s Secret of type `docker-registry`
- reference it via `imagePullSecrets` in a Deployment

## Prerequisites
- `docker`, `kubectl`, AWS CLI configured (`aws sts get-caller-identity`)
- A Kubernetes cluster (Minikube is OK)

## Step-by-step (commands)

### 1) Set region and create repo
```bash
export AWS_REGION=eu-north-1
aws ecr create-repository --repository-name private-demo --region $AWS_REGION
```

### 2) Login Docker to ECR
```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
aws ecr get-login-password --region $AWS_REGION \
| docker login --username AWS --password-stdin $ECR_REGISTRY
```

### 3) Tag and push
```bash
export IMAGE_URI="$ECR_REGISTRY/private-demo:1.0"
docker tag private-demo:1.0 $IMAGE_URI
docker push $IMAGE_URI
```

### 4) Create namespace and imagePullSecret
```bash
kubectl create namespace demo
kubectl -n demo create secret docker-registry ecr-regcred \
  --docker-server=$ECR_REGISTRY \
  --docker-username=AWS \
  --docker-password="$(aws ecr get-login-password --region $AWS_REGION)"
```

### 5) Deploy
Edit `app.yaml` and set the image to `$IMAGE_URI`, then:
```bash
kubectl -n demo apply -f app.yaml
kubectl -n demo get pods -w
```

## Files
- `app.yaml` — example Deployment + Service wired to `imagePullSecrets`

## Verification
```bash
kubectl -n demo describe pod -l app=private-demo
kubectl -n demo get deploy,svc
```

## Cleanup
```bash
kubectl delete namespace demo
aws ecr delete-repository --repository-name private-demo --region $AWS_REGION --force
```

## Real DevOps notes
- Private registries are standard in enterprise (ECR/ACR/GCR/Artifactory/Nexus).
- For production, use:
  - image signing / provenance (Cosign, SLSA)
  - least-privilege IAM for pulling
  - automated vulnerability scanning + admission control
- `aws sts get-caller-identity` must work

## Step-by-step (example region: eu-north-1)

### 1) Create repo
```bash
export AWS_REGION=eu-north-1
aws ecr create-repository --repository-name private-demo --region $AWS_REGION
```

### 2) Login Docker to ECR
```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
```

### 3) Tag & push image
```bash
export IMAGE_URI="$ECR_REGISTRY/private-demo:1.0"
docker tag private-demo:1.0 $IMAGE_URI
docker push $IMAGE_URI
```

### 4) Create the registry Secret
```bash
kubectl create namespace demo
kubectl -n demo create secret docker-registry ecr-regcred \
  --docker-server=$ECR_REGISTRY \
  --docker-username=AWS \
  --docker-password="$(aws ecr get-login-password --region $AWS_REGION)"
```

### 5) Deploy
Update `app.yaml` with your `IMAGE_URI` and apply:
```bash
kubectl -n demo apply -f app.yaml
kubectl -n demo get pods -w
```

## Verification
- Pod reaches `Running` and does not show `ErrImagePull`/`ImagePullBackOff`.
- `kubectl -n demo describe pod <pod>` shows successful image pull.

## Cleanup
```bash
kubectl delete namespace demo
# Optional: delete repo (stops all storage charges)
aws ecr delete-repository --repository-name private-demo --region $AWS_REGION --force
```

## Real DevOps notes
- Private registries are standard in production (ECR/ACR/GCR/Harbor/Nexus).
- Best practice: enable **image scanning**, restrict IAM, and use immutable tags plus signed images.
