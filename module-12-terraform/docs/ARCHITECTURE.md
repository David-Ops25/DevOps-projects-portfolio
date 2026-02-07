# Architecture Notes (Module 12)

## Demo 1 & 2: EC2 + Docker deployment
Terraform provisions VPC + subnet + routing + security group + EC2.
EC2 user_data installs Docker/Compose and starts an nginx container on port 80.

## Demo 3: EKS cluster
Terraform provisions VPC and EKS cluster with a managed node group.

## Demo 5: Remote state
Terraform state stored in S3 and locked with DynamoDB.
