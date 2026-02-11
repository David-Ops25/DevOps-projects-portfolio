# Challenges & Solutions — Module 14

## Instances Recreated Automatically
**Cause:** EKS-managed Auto Scaling Group  
**Solution:** Scaled ASG to zero and deleted nodegroup before deleting EKS cluster.

## Lost SSH Access
**Cause:** Incorrect key / security group  
**Solution:** Used EC2 Instance Connect and root volume recovery.

## Hidden AWS Costs
**Cause:** EKS control plane and unattached EBS volumes  
**Solution:** Full CLI audit and cleanup after demos.