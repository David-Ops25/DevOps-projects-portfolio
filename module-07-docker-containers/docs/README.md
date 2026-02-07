# Docker + Compose Demo Stack

## What this project is about
Containerize a Node.js app, run it with MongoDB + Mongo Express locally using Docker and Docker Compose, persist data with volumes, and publish images to private registries (Nexus/ECR).

## What was done (implementation summary)
- Wrote Dockerfile for Node.js app
- Created docker-compose.yml for Node + MongoDB + Mongo Express
- Added volume for MongoDB persistence
- Configured registry auth (Nexus/ECR)
- Deployed stack to a remote server using docker compose

## Challenges faced & fixes
- App couldn't reach MongoDB → fixed container networking/ENV vars
- Volume permissions → adjusted MongoDB volume mount
- Private registry pull denied → docker login + correct tags

## Files in this folder
See: [`files.md`](../docs/files.md)

## Commands used
See: [`../logs/commands.md`](../logs/commands.md)

## Next improvements (optional)
- Add healthchecks + restart policies
- Add CI pipeline to build/push image
- Secure secrets with Docker secrets or vault
