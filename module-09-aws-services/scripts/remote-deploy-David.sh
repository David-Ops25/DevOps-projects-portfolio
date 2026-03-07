#!/usr/bin/env bash
set -euo pipefail

cd /opt/app
docker compose pull
docker compose up -d
docker image prune -f
