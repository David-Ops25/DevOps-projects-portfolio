# Module 9 Runbook (Step‑by‑Step Commands)

This runbook is written to reproduce the Module 9 demos end‑to‑end in a clean AWS account.
It is intentionally explicit: **commands, syntax, and verification**.

> Note: Replace placeholders like `<JENKINS_EC2_PUBLIC_IP>` and `<APP_EC2_PUBLIC_IP>`.

---

## 0) Prerequisites
- AWS account + IAM user with enough permissions for EC2 (for learning): `AmazonEC2FullAccess`
- A chosen region (example used in the project: `eu-north-1`)
- Local machine with SSH client + Git

---

## 1) Create EC2 instances (Jenkins + App Server)

### How many EC2 instances?
Minimum recommended:
- **2 EC2 instances**
  1. Jenkins server (Dockerized Jenkins)
  2. App server (Docker + Docker Compose)

### Instance notes
- AMI: Amazon Linux 2023 or Amazon Linux 2 for the EC2 hosts
- Instance type: t3.micro (lab) or t3.small (more comfortable)
- Security groups:
  - Jenkins SG inbound: 22 (SSH), 8080 (Jenkins UI), 50000 (agent if needed)
  - App SG inbound: 22 (SSH), 3000 (app), 8081 (mongo-express)

---

## 2) SSH key pair and access

### Find your key file
```bash
find ~ -maxdepth 3 -type f -name "*.pem" 2>/dev/null
```

### Correct permissions (Linux/macOS/WSL)
```bash
chmod 400 ~/.ssh/aws-key-pair.pem
```

### SSH to server
```bash
ssh -i ~/.ssh/aws-key-pair.pem ec2-user@<EC2_PUBLIC_IP>
```

---

## 3) Install Docker on EC2 hosts (Jenkins server + App server)

### Amazon Linux (host OS)
```bash
sudo yum update -y
sudo yum install -y docker
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ec2-user
newgrp docker
docker version
```

---

## 4) Run Jenkins as a Docker container on the Jenkins EC2 host

### Start Jenkins container with Docker socket mount
This enables the Jenkins container to run Docker commands on the host Docker daemon.

```bash
docker run -d \
  --name jenkins \
  --restart unless-stopped \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### (If Docker socket permission denied happens)
Check the host docker group GID:
```bash
getent group docker
```

Restart Jenkins with group-add (example uses GID 992):
```bash
docker stop jenkins
docker rm jenkins

docker run -d \
  --name jenkins \
  --restart unless-stopped \
  -p 8080:8080 \
  -p 50000:50000 \
  --group-add 992 \
  -v /var/jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

---

## 5) Install Docker CLI inside Jenkins container (required for docker build)

```bash
docker exec -it -u 0 jenkins bash
```

Inside container (Debian):
```bash
apt-get update
apt-get install -y docker.io
docker --version
exit
```

Verify Jenkins can speak to Docker daemon:
```bash
docker exec jenkins docker version
```

---

## 6) Fix SSH from Jenkins to the App server (deploy key approach)

### Generate a dedicated deploy key (on your laptop)
```bash
ssh-keygen -t ed25519 -f ~/jenkins-deploy-key -C "jenkins-deploy"
```

Copy public key to app server (from laptop):
```bash
ssh-copy-id -i ~/jenkins-deploy-key.pub -o StrictHostKeyChecking=no ec2-user@<APP_EC2_PUBLIC_IP>
```

Manual verify:
```bash
ssh -i ~/jenkins-deploy-key ec2-user@<APP_EC2_PUBLIC_IP> "whoami && hostname"
```

### Jenkins credentials
- Jenkins → Manage Jenkins → Credentials → Global → Add Credentials
- **Kind:** Secret file
- Upload private key file `jenkins-deploy-key`
- ID: `jenkins-deploy-key`

---

## 7) Install Docker + Docker Compose on App server

Docker already installed earlier. Compose plugin is usually available as `docker compose`:
```bash
docker compose version
```

---

## 8) Demo: Deploy app + MongoDB + Mongo Express on App server (Compose)
A template compose file is provided in this repo: `docker/docker-compose.yml`.

Manual test (app server):
```bash
mkdir -p ~/demo2
cd ~/demo2
# create docker-compose.yml
docker compose up -d
docker ps
```

Access:
- App: `http://<APP_EC2_PUBLIC_IP>:3000`
- Mongo Express: `http://<APP_EC2_PUBLIC_IP>:8081`

---

## 9) GitHub checkout from Jenkins
Add GitHub Personal Access Token (PAT) in Jenkins credentials:
- Kind: Username with password (or Secret text)
- ID: `github-pat`

Pipeline checkout snippet:
```groovy
git(url: 'https://github.com/<ORG>/<REPO>.git', branch: 'main', credentialsId: 'github-pat')
```

---

## 10) Docker Hub push from Jenkins
Create credentials:
- Kind: Username with password
- ID: `dockerhub-creds`

Push snippet:
```bash
echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
docker push davidangyu/jenkins-cicd-demo-app:${BUILD_NUMBER}
docker logout
```

---

## 11) Install AWS CLI v2 on developer workstation (Ubuntu/WSL)
```bash
cd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
sudo apt-get update && sudo apt-get install -y unzip
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

Configure (do NOT share keys publicly):
```bash
aws configure
aws sts get-caller-identity
```

---

## 12) Install AWS CLI inside Jenkins container + bind credentials
Inside container (root):
```bash
cd /tmp
apt-get update
apt-get install -y curl unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
unzip awscliv2.zip
./aws/install
aws --version
```

Jenkins plugins:
- AWS Credentials
- Pipeline: AWS Steps (AWS Steps)

Create Jenkins credential:
- Kind: **AWS Credentials**
- ID: `aws-jenkins`

Pipeline verification:
```groovy
withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-jenkins']]) {
  sh 'aws sts get-caller-identity'
}
```

---

## 13) Full CI/CD Pipeline (build → push → deploy → smoke test)
Use the complete Jenkinsfile templates in `pipelines/`.

- `pipelines/Jenkinsfile-ci-cd-dockerhub-ec2.groovy`
- `pipelines/Jenkinsfile-deploy-only.groovy`

