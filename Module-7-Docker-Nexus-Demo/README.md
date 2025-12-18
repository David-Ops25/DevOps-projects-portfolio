# Module 7 – Docker & Nexus Registry Demo

## Overview
This project demonstrates containerisation and image management using Docker and Nexus Repository Manager.

> I containerised a Node.js application, orchestrated it with Docker Compose, deployed a private Nexus Docker registry on a cloud VM, secured it with roles and users, and pushed production-ready Docker images to it.

## What This Module Covers
- Dockerfile for Node.js application
- Multi-container orchestration with Docker Compose
- Docker volumes and networking
- Private Docker registry using Nexus
- Authentication and role-based access
- Pushing Docker images to Nexus
- Bonus: Pulling and running image on a remote server

## Architecture
Local Machine:
- Build Docker image
- Push image to Nexus

Cloud VM:
- Nexus Repository Manager (Docker registry)
- Pull and run application image

## Repository Structure
See folder layout for scripts, configs, and documentation.

## How to Run (Summary)
1. Build image locally
2. Push to Nexus
3. Pull from Nexus on server
4. Run container

## Status
✅ Module 7 Complete (including bonus remote deployment)
