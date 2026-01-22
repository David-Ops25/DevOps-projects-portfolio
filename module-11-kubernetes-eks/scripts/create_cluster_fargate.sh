#!/usr/bin/env bash
set -euo pipefail
eksctl create cluster -f eksctl/cluster-fargate.yaml
