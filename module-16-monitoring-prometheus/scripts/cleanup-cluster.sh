#!/usr/bin/env bash
set -euo pipefail

eksctl delete cluster --name monitoring-cluster --region eu-north-1
