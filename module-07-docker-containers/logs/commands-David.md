# Commands Used

> Add your real command history here. The blocks below are safe templates.

## Build & run locally
```bash
docker build -t node-app:local ./app
docker run --rm -p 3000:3000 node-app:local
```

## Run with Docker Compose
```bash
cd configs/docker-compose
cp .env.example .env
docker compose up -d
docker compose ps
curl http://localhost:3000
```

## Persist data with volumes
```bash
docker volume ls
docker volume inspect mongo-data
```

## Push to registry (Nexus/ECR)
```bash
docker tag node-app:local <REGISTRY>/<REPO>:v1
docker login <REGISTRY>
docker push <REGISTRY>/<REPO>:v1
```
