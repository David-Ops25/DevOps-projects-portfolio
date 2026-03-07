#!/usr/bin/env bash
set -euo pipefail

CLUSTER_NAME="monitoring-cluster"
REGION="eu-north-1"
NODEGROUP_NAME="workers"
NODE_TYPE="t3.medium"
NODE_COUNT="2"

aws sts get-caller-identity >/dev/null

eksctl create cluster \
  --name "$CLUSTER_NAME" \
  --region "$REGION" \
  --nodegroup-name "$NODEGROUP_NAME" \
  --node-type "$NODE_TYPE" \
  --nodes "$NODE_COUNT"
