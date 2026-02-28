#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR/terraform"

echo "Destroying AWS resources created by Terraform..."
terraform destroy -auto-approve

echo "Done. Verify in AWS console that no EC2 instances, EBS volumes, or EIPs remain." 
