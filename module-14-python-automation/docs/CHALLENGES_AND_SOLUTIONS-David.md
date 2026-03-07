# Challenges & Solutions — Module 14

This module intentionally includes **real-world operational problems** and the fixes.

---

## 1) Region mismatch (resources “missing”)
**Symptom:** AWS CLI default region was `eu-north-1`, but EC2/EKS resources lived in `us-east-1`.  
**Fix:** Run with explicit region or export `AWS_REGION=us-east-1`.

---

## 2) Lost SSH access (permission denied / timeouts)
**Symptom:** SSH returned `Permission denied (publickey)` or port 22 timeouts.  
**Fixes applied:**
- Verified security group ingress CIDR and port 22 reachability
- Used **EC2 Instance Connect** to push a temporary key and regain access
- Made access permanent by appending the public key to `~/.ssh/authorized_keys`

---

## 3) “Instance keeps getting recreated”
**Symptom:** After terminating an instance, another appeared automatically.  
**Root cause:** EKS managed nodegroup uses an Auto Scaling Group with DesiredCapacity > 0.  
**Fix:** Delete the EKS nodegroup (or scale desired capacity to 0) before terminating nodes.

---

## 4) EKS deletion blocked
**Symptom:** `ResourceInUseException: Cluster has nodegroups attached`  
**Fix:** Delete nodegroups first, wait for deletion, then delete the cluster.

---

## 5) Hidden AWS costs
**Sources:**
- EKS control plane (billed while cluster exists)
- Unattached EBS volumes (`State=available`)
- EBS snapshots

**Fix:** End-of-module audit and teardown:
- EC2: terminate instances
- EBS: delete unattached volumes + snapshots
- EKS: delete nodegroups + cluster
