# Terraform -> Ansible integration demo
# This runs Ansible on the control node after infrastructure is provisioned.

resource "null_resource" "ansible_configure" {
  depends_on = [
    aws_instance.control,
    aws_instance.managed,
    aws_instance.nexus
  ]

  provisioner "local-exec" {
    command = <<EOT
set -e

CONTROL_IP="${aws_instance.control.public_ip}"
KEY="${pathexpand("~/.ssh/ansible-key-pair.pem")}" 

# Wait for SSH
until ssh -o StrictHostKeyChecking=no -i "$KEY" ubuntu@$CONTROL_IP "echo SSH_OK" >/dev/null 2>&1; do
  sleep 5
done

# Sync Ansible project to control node (expect repo cloned locally)
rsync -avz -e "ssh -o StrictHostKeyChecking=no -i $KEY" \
  --exclude ".git" --exclude ".terraform" \
  ../ansible/ \
  ubuntu@$CONTROL_IP:/home/ubuntu/module15-ansible/

# Run playbook
ssh -o StrictHostKeyChecking=no -i "$KEY" ubuntu@$CONTROL_IP "
  set -e
  cd ~/module15-ansible
  source ~/ansible-venv/bin/activate || true
  ansible-playbook site.yml
"
EOT
  }
}
