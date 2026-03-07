# Kubernetes Manifests + Helm

## What this project is about
Work with Kubernetes manifests, config management (ConfigMaps/Secrets), Helm charts, private image pulls, and multi-service deployments.

## What was done (implementation summary)
- Set up minikube
- Deployed MongoDB + MongoExpress using manifests
- Created ConfigMap + Secret and mounted them
- Deployed stateful MongoDB via Helm (with persistence)
- Deployed Mosquitto with config/secret volumes
- Pulled image from private registry using imagePullSecret
- Structured deployments with Helm and Helmfile

## Challenges faced & fixes
- Pods pending due to missing resources → increased minikube resources
- ImagePullBackOff → fixed secret and image URL
- PVC pending → provisioned storage class / correct values in Helm

## Files in this folder
See: [`files.md`](../docs/files.md)

## Commands used
See: [`../logs/commands.md`](../logs/commands.md)

## Next improvements (optional)
- Add ingress controller + TLS
- Add HPA + resource limits
- Add GitOps (ArgoCD/Flux)
