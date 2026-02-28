# Challenges Faced & Solutions

This project was built in a realistic environment (AWS EC2) and encountered real operational issues. Below is a concise log of the most important ones and how they were solved.

## 1) Security Group replacement stuck during Terraform apply
**Symptom**: Terraform hung for several minutes while destroying a Security Group.

**Cause**: AWS will not delete an SG if any ENIs or instances still reference it.

**Fix**:
- Used `name_prefix` so Terraform can create a new SG before destroying the old one.
- Added lifecycle rule:

```hcl
lifecycle {
  create_before_destroy = true
}
```

## 2) Dynamic Inventory failing with old Ansible (2.10)
**Symptom**: `amazon.aws` inventory plugin failed with errors like:
- collection not supported
- `get_options` attribute missing

**Cause**: The control node shipped with an older Ansible version.

**Fix**: Installed modern Ansible in a virtualenv on the control node:

```bash
python3 -m venv ~/ansible-venv
source ~/ansible-venv/bin/activate
pip install --upgrade pip
pip install "ansible-core>=2.15,<2.18" ansible boto3 botocore
ansible-galaxy collection install amazon.aws
```

## 3) Nexus registry port 8083 not accessible
**Symptom**: Nexus container was running but only mapped port 8081.

**Fix**: Recreated container exposing both ports:

```bash
docker rm -f nexus || true
docker run -d --name nexus --restart=always \
  -p 8081:8081 -p 8083:8083 \
  -v /opt/nexus-data:/nexus-data \
  sonatype/nexus3:latest
```

## 4) Docker registry timeouts from EC2 instances
**Symptom**: `docker login <public-ip>:8083` timed out from another EC2.

**Cause**: Security group allowed 8083 only from the operator’s public IP, not from EC2 peers.

**Fix**:
- Use **private IP** for EC2-to-EC2 traffic: `<nexus-private-ip>:8083`
- Ensure SG allows internal traffic (`self = true`).

## 5) Docker login returns 401 Unauthorized
**Symptom**: `docker login <nexus-private-ip>:8083` returned 401.

**Cause**: Wrong credentials or missing Nexus privileges.

**Fix**:
- Created a least-privilege Nexus user (e.g., `dockeruser`).
- Assigned privileges for `docker-hosted` repo.
- Enabled Docker Bearer Token Realm if needed.

## 6) Docker package conflict (docker.io vs docker-ce)
**Symptom**: Ansible `apt install docker.io` failed with `containerd.io conflicts: containerd`.

**Cause**: Host already had docker-ce/containerd.io installed; Ubuntu `docker.io` conflicts.

**Fix**: Nexus role does **not** force-install docker.io; it checks docker and starts service.

## 7) Jenkins repository key errors
**Symptom**: Jenkins apt repository reported `NO_PUBKEY ...` and refused to install.

**Fix**: Add Jenkins key using `/etc/apt/keyrings` and reference it with `signed-by=...`.

---

These challenges were addressed in a way that matches real DevOps operations: fix root causes, keep automation idempotent, and avoid brittle assumptions.
