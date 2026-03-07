# Jenkins CI Pipelines

## What this project is about
Set up Jenkins and build CI pipelines for a Java Maven app: compile, test, build JAR, build Docker image, push to Docker Hub, and automate triggers/versioning.

## What was done (implementation summary)
- Ran Jenkins as Docker container
- Installed tools (Maven/Node) and enabled Docker builds
- Built Pipeline + Multibranch jobs using Jenkinsfile
- Created Jenkins Shared Library to reuse pipeline steps
- Configured webhooks to trigger builds
- Implemented dynamic versioning and prevented commit loops

## Challenges faced & fixes
- Docker permission errors in Jenkins → mounted docker.sock or used Docker-in-Docker
- Missing build tools → installed Maven/Node in Jenkins agent
- Webhook not triggering → verified Git webhook URL + secret token

## Files in this folder
See: [`files.md`](../docs/files.md)

## Commands used
See: [`../logs/commands.md`](../logs/commands.md)

## Next improvements (optional)
- Add code quality checks (SonarQube)
- Use ephemeral agents (Kubernetes)
- Add approvals for production deploy
