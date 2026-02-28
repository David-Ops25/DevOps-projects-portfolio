# Commands & Syntax Used (Module 15)

This file is a consolidated command log for the module.

> Replace placeholder values like `<CONTROL_PUBLIC_IP>` with Terraform outputs.

---

## Terraform (AWS)

### Initialize & apply
```bash
cd terraform
terraform fmt
terraform init
terraform apply -auto-approve
```

### Destroy (stop billing)
```bash
cd terraform
terraform destroy -auto-approve
```

---

## SSH

```bash
ssh -i ~/.ssh/ansible-key-pair.pem ubuntu@<CONTROL_PUBLIC_IP>
ssh -i ~/.ssh/ansible-key-pair.pem ubuntu@<NODE_PUBLIC_IP>
```

---

## Ansible – virtualenv (control node)

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
python3 -m venv ~/ansible-venv
source ~/ansible-venv/bin/activate
pip install --upgrade pip
pip install "ansible-core>=2.15,<2.18" ansible boto3 botocore
ansible-galaxy collection install amazon.aws
```

---

## Dynamic inventory (AWS EC2)

```bash
cd ~/module15-ansible
ansible-inventory --graph
ansible all -m ping
ansible role_ansible_managed -m ping
ansible role_nexus -m ping
```

---

## Run the main deployment

```bash
ansible-playbook site.yml
```

---

## Nexus registry push (from a managed node)

Use **private** IP for EC2-to-EC2 registry operations.

```bash
sudo docker login <NEXUS_PRIVATE_IP>:8083
sudo docker pull nginx:latest
sudo docker tag nginx:latest <NEXUS_PRIVATE_IP>:8083/nginx-test:1.0
sudo docker push <NEXUS_PRIVATE_IP>:8083/nginx-test:1.0
```

---

## Kubernetes (K3s)

### Install cluster
```bash
ansible-playbook k8s_k3s_cluster.yml
```

### Deploy nginx
```bash
ansible-playbook k8s_deploy_nginx.yml
```

### Verify
```bash
ansible name_configuration_management_ansible_node1 -b -a "k3s kubectl get nodes -o wide"
```

### Test service
```bash
curl -I http://<NODE1_PRIVATE_IP>:30080
```

---

## Jenkins → Ansible trigger (concept)

Jenkins does not need Ansible installed. It SSHs to the control node and runs:

```bash
source ~/ansible-venv/bin/activate
cd ~/module15-ansible
ansible-playbook site.yml
```

---
