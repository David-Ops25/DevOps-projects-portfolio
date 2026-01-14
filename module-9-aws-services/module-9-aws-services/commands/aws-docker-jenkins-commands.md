# Command Reference (Module 9)

## Linux permissions for SSH keys
chmod 400 ~/.ssh/aws-key-pair.pem

## Find PEM keys
find ~ -maxdepth 3 -type f -name "*.pem" 2>/dev/null

## Docker on Amazon Linux
sudo yum install -y docker
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ec2-user
newgrp docker

## Run Jenkins in Docker
docker run -d --name jenkins --restart unless-stopped -p 8080:8080 -p 50000:50000 \
  -v /var/jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

## Install Docker CLI inside Jenkins container (Debian)
docker exec -it -u 0 jenkins bash
apt-get update && apt-get install -y docker.io

## AWS CLI v2 (Ubuntu/WSL)
cd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
sudo apt-get update && sudo apt-get install -y unzip
unzip awscliv2.zip
sudo ./aws/install

## Validate AWS identity
aws sts get-caller-identity
