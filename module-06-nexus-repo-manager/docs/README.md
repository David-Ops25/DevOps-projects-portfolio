# Run Nexus + Publish Artifacts

## What this project is about
Install and configure Sonatype Nexus Repository Manager on a cloud server and publish Java artifacts built with Gradle and Maven.

## What was done (implementation summary)
- Installed Nexus and configured it to run as a service
- Created hosted repositories (Maven/Gradle)
- Created roles/users with least privilege
- Configured `settings.xml` (Maven) and `gradle.properties` (Gradle) for auth
- Built and uploaded artifacts

## Challenges faced & fixes
- Nexus not reachable → opened port 8081/firewall
- Upload auth errors → fixed credentials + repository URL
- Wrong groupId/artifactId paths → verified coordinates in build files

## Files in this folder
See: [`files.md`](../docs/files.md)

## Commands used
See: [`../logs/commands.md`](../logs/commands.md)

## Next improvements (optional)
- Enable HTTPS with reverse proxy
- Set up blobstore cleanup policies
- Add Docker hosted repo (Module 7)
