data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

locals {
  azs = ["${var.region}a", "${var.region}b"]
}

module "vpc" {
  source = "../../modules/vpc"
  name           = var.name
  cidr           = "10.20.0.0/16"
  azs            = local.azs
  public_subnets = ["10.20.1.0/24", "10.20.2.0/24"]
  private_subnets= ["10.20.101.0/24", "10.20.102.0/24"]
  tags = var.tags
}

module "ec2" {
  source = "../../modules/ec2"
  name          = "${var.name}-web"
  ami_id        = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id     = module.vpc.public_subnets[0]
  vpc_id        = module.vpc.vpc_id
  key_name      = var.key_name
  user_data = <<'USERDATA'
#!/bin/bash
set -euo pipefail

apt-get update -y
apt-get install -y ca-certificates curl gnupg lsb-release

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable"   | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

systemctl enable docker
systemctl start docker

mkdir -p /opt/app
cat > /opt/app/docker-compose.yml <<'EOF'
version: "3.8"
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
EOF

cd /opt/app
docker compose up -d

USERDATA
  tags = var.tags
}
