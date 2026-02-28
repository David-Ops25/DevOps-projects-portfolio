# Module 15 – Configuration Management with Ansible (AWS Edition)

This repository is a **complete, portfolio-ready implementation of Module 15** (Configuration Management with Ansible).

Instead of DigitalOcean, this project uses **AWS EC2** as the infrastructure platform.

It demonstrates an end-to-end DevOps workflow:

- **Terraform** provisions infrastructure on AWS
- **Ansible** configures servers using **roles**
- **Dynamic Inventory** discovers EC2 instances automatically using tags
- **Nexus Repository Manager** runs as a Docker container and hosts a **Docker registry**
- A **Node.js application** is deployed and managed by **systemd** (non-root)
- **Kubernetes (K3s)** cluster is automated and an application is deployed
- **Jenkins** triggers Ansible (CI/CD entry point)

>  **Security note:** This repo does **not** include any AWS credentials or SSH private keys for security reasons.

---

## What Module 15 is about

Module 15 focuses on **configuration management** and **automation** using Ansible:

- provisioning infrastructure (here done with Terraform)
- repeatable configuration of servers (packages, users, services)
- structuring automation with **roles**
- reducing manual work through **dynamic inventory**
- integrating Ansible into common DevOps tools (Terraform, Docker, Kubernetes, Jenkins)

---

## Demos covered (Module 15)

This repo covers all demos:

1. **Automate Node.js Application Deployment** ✅
2. **Automate Nexus Deployment** ✅
3. **Ansible & Docker (Push to Nexus Docker registry)** ✅
4. **Configure Dynamic Inventory (AWS EC2 plugin)** ✅
5. **Structure Playbooks with Ansible Roles** ✅
6. **Ansible Integration in Terraform** ✅
7. **Automate Kubernetes Deployment (K3s)** ✅
8. **Ansible Integration in Jenkins (Pipeline)** ✅

---

## Repository structure

```
.
├─ terraform/                     # AWS infrastructure (EC2, SG, outputs)
├─ ansible/                       # Ansible automation (roles, playbooks, inventory)
│  ├─ ansible.cfg
│  ├─ inventory/aws_ec2.yml        # Dynamic inventory
│  ├─ site.yml                     # One-command deployment
│  ├─ roles/
│  ├─ k8s_k3s_cluster.yml
│  ├─ k8s_deploy_nginx.yml
│  └─ jenkins/Jenkinsfile          # Jenkins pipeline example
├─ docs/
│  ├─ CHALLENGES.md
│  └─ COMMANDS.md
└─ scripts/
   └─ destroy.sh                   # Safe cleanup helper
```

---

## Prerequisites

### Local machine
- Terraform (1.x)
- AWS CLI configured (`aws configure`)
- An SSH key pair uploaded to AWS (EC2 key pair name)

### AWS
- An AWS account
- Permissions for EC2, VPC, Security Groups

---

## Quickstart

### 1) Configure Terraform variables

Create `terraform/terraform.tfvars`:

```hcl
aws_region   = "us-east-1"
project_name = "configuration-management-ansible"
key_name     = "ansible-key-pair"          # EC2 Key Pair name
my_ip_cidr   = "YOUR_PUBLIC_IP/32"         # e.g. 82.20.156.133/32
```

### 2) Provision infrastructure

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

Terraform outputs the public IPs for:
- control node
- managed nodes
- nexus
- jenkins

### 3) Configure the control node (Ansible)

SSH into the control node and run Ansible from there.

```bash
ssh -i ~/.ssh/ansible-key-pair.pem ubuntu@<CONTROL_PUBLIC_IP>

# Activate venv used for modern Ansible + AWS inventory
source ~/ansible-venv/bin/activate
cd ~/module15-ansible

ansible-inventory --graph
ansible-playbook site.yml
```

### 4) Nexus Docker registry demo

- Nexus UI: `http://<NEXUS_PUBLIC_IP>:8081`
- Create Docker hosted repo on port **8083**
- Use **private IP** for EC2-to-EC2 pushes:

```bash
sudo docker login <NEXUS_PRIVATE_IP>:8083
sudo docker pull nginx:latest
sudo docker tag nginx:latest <NEXUS_PRIVATE_IP>:8083/nginx-test:1.0
sudo docker push <NEXUS_PRIVATE_IP>:8083/nginx-test:1.0
```

### 5) Kubernetes (K3s) demo

```bash
cd ansible
ansible-playbook k8s_k3s_cluster.yml
ansible-playbook k8s_deploy_nginx.yml

# Test from control node (node1 private ip + NodePort 30080)
curl -I http://<NODE1_PRIVATE_IP>:30080
```

### 6) Jenkins demo

- Jenkins UI: `http://<JENKINS_PUBLIC_IP>:8080`
- Create pipeline using `ansible/jenkins/Jenkinsfile`
- Jenkins will SSH to the control node and run `ansible-playbook site.yml`

---

## Challenges faced & solutions (real-world issues)

See **docs/CHALLENGES.md** for a detailed write-up.

Highlights:
- **Security group replacement stuck** → fixed with `name_prefix` + `create_before_destroy`
- **Dynamic inventory failing** due to old Ansible → fixed with Python venv and modern `ansible-core`
- **Nexus Docker port 8083 not exposed** → recreated container with `-p 8083:8083`
- **Docker registry timeouts** when using public IP → used private IP and SG self-traffic rules
- **Docker auth 401** → created least-privilege Nexus user and enabled Docker realm
- **Docker package conflicts** (docker.io vs docker-ce) → stopped installing docker.io when docker-ce already present
- **Jenkins apt repo key errors** → corrected keyring setup on Jenkins host

---

## Commands & syntax used

A complete, copy-paste command log is included:
- **docs/COMMANDS.md**

---

## Cleanup (stop billing)

```bash
cd terraform
terraform destroy -auto-approve
```

Or run:

```bash
./scripts/destroy.sh
```

---

## License

MIT – see [LICENSE](LICENSE).
