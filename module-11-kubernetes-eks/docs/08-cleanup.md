# Cleanup Guide

## Delete cluster
eksctl delete cluster --name <CLUSTER_NAME> --region eu-north-1

## Verify no leftovers
aws cloudformation list-stacks --region eu-north-1
aws ec2 describe-nat-gateways --region eu-north-1
aws elbv2 describe-load-balancers --region eu-north-1
