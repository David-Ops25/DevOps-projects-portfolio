# Commands used in Module 8
🔹 Docker & Jenkins Setup
docker run -d \
  --name jenkins \
  --privileged \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

🔹 Access Jenkins Container
docker exec -it jenkins bash

🔹 Check Docker Inside Jenkins
docker --version
docker ps

🔹 Fix Docker Permissions
docker exec -u root -it jenkins bash

id
getent group docker

🔹 Run Nexus Repository
docker run -d \
  --name nexus \
  -p 8081:8081 \
  -p 8083:8083 \
  -v nexus-data:/nexus-data \
  sonatype/nexus3

🔹 Get Nexus Admin Password
docker exec -it nexus cat /nexus-data/admin.password

🔹 Docker Login to Nexus
docker login <droplet-ip>:8083

🔹 Build Docker Image Locally
docker build -t module8-demo:1 .

🔹 Tag Image for Nexus
docker tag module8-demo:1 <droplet-ip>:8083/module8-demo:1

🔹 Push Image to Nexus
docker push <droplet-ip>:8083/module8-demo:1

🔹 Git & Jenkins Integration
git add .
git commit -m "Add Module 8: Jenkins CI/CD with Docker and Nexus"
git push origin main
