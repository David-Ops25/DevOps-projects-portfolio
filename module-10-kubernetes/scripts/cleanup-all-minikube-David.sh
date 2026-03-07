#!/usr/bin/env bash
set -euo pipefail

namespaces=(mongo-demo mongo-demo mongo-demo micro demo)

for ns in "${namespaces[@]}"; do
  if kubectl get ns "$ns" >/dev/null 2>&1; then
    echo "Deleting namespace: $ns"
    kubectl delete ns "$ns" --wait=false
  fi
done

echo "Cleanup requested. Use 'kubectl get ns' to watch termination."
