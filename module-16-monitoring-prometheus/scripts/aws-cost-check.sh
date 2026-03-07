#!/usr/bin/env bash
set -euo pipefail

for REGION in eu-north-1 us-east-1; do
  echo "===== Region: ${REGION} ====="
  aws eks list-clusters --region "$REGION"
  aws ec2 describe-instances --region "$REGION" --query 'Reservations[].Instances[?State.Name==`running`].[InstanceId,InstanceType]'
  aws ec2 describe-volumes --region "$REGION" --query 'Volumes[?State==`available`].[VolumeId,Size]'
  aws elbv2 describe-load-balancers --region "$REGION" --query 'LoadBalancers[].LoadBalancerArn'
  aws ec2 describe-addresses --region "$REGION"
  aws ec2 describe-nat-gateways --region "$REGION" --query 'NatGateways[].State'
  echo
 done
