#!/usr/bin/env bash
set -euo pipefail
CLUSTER="${1:?cluster name}"
REGION="${2:-eu-north-1}"
eksctl delete cluster --name "${CLUSTER}" --region "${REGION}"
