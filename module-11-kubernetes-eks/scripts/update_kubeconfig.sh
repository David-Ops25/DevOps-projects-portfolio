#!/usr/bin/env bash
set -euo pipefail
CLUSTER="${1:?cluster name}"
REGION="${2:-eu-north-1}"
aws eks update-kubeconfig --region "${REGION}" --name "${CLUSTER}"
kubectl cluster-info
