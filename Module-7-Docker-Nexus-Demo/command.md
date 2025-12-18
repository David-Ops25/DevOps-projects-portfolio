Module 7 – Commands Reference (Docker & Nexus)

This document lists all the key commands used throughout Module 7 demos, from Docker basics to Nexus registry integration and remote deployment.

🔹 Phase 1: Docker Basics & Dockerfile Demo
# Check Docker installation
docker --version

# Build Docker image
docker build -t module7-dockerfile-demo:1.0 .

# List images
docker images

# Run container locally
docker run -d -p 3000:3000 --name module7-app module7-dockerfile-demo:1.0

# Check running containers
docker ps

# Stop and remove container
docker stop module7-app
docker rm module7-app

🔹 Phase 2: Docker Compose (Multi-Container App)
# Start services
docker compose up -d

# View running services
docker compose ps

# View logs
docker compose logs

# Stop services
docker compose down

# Remove volumes (optional)
docker compose down -v

🔹 Phase 3: Nexus Repository (Docker Registry)
Run Nexus on Cloud VM
# Run Nexus container
docker run -d \
  --name nexus \
  -p 8081:8081 \
  -p 8083:8083 \
  -v nexus-data:/nexus-data \
  sonatype/nexus3

Verify Nexus
# Check container
docker ps

# View logs
docker logs nexus

# Exec into container
docker exec -it nexus bash

🔹 Phase 4: Nexus Admin Setup
# Get admin password
docker exec -it nexus cat /nexus-data/admin.password


Then (via UI):

Login to http://<VM-IP>:8081

Change admin password

Disable anonymous access

Create Docker hosted repository (port 8083)

Create roles and users for Docker push/pull

🔹 Phase 5: Docker Client Configuration
Configure insecure registry (HTTP)
sudo nano /etc/docker/daemon.json

{
  "insecure-registries": ["<VM-IP>:8083"]
}

# Restart Docker
sudo systemctl restart docker

🔹 Phase 6: Login, Tag & Push Image to Nexus
# Login to Nexus registry
docker login <VM-IP>:8083

# Tag image
docker tag module7-dockerfile-demo:1.0 <VM-IP>:8083/module7-demo:1.0

# Push image
docker push <VM-IP>:8083/module7-demo:1.0

🔹 Phase 7: Bonus – Remote Pull & Run (Optional Demo)
# Login from remote server
docker login <VM-IP>:8083

# Pull image
docker pull <VM-IP>:8083/module7-demo:1.0

# Run container
docker run -d -p 3000:3000 <VM-IP>:8083/module7-demo:1.0

🔹 Phase 8: Cleanup & Validation
# List containers
docker ps -a

# Stop Nexus
docker stop nexus

# Remove Nexus container
docker rm nexus

# List volumes
docker volume ls