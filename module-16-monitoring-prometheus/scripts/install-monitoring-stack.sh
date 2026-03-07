#!/usr/bin/env bash
set -euo pipefail

kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
helm repo update
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack -n monitoring
