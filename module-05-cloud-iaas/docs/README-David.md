# Droplet Setup + Java Gradle Deployment

## What this project is about
Provision a cloud VM (DigitalOcean Droplet), apply Linux security best practices (non-root user), and deploy a Java Gradle application as a service.

## What was done (implementation summary)
- Created droplet and configured firewall
- Created non-root sudo user
- Installed Java + Gradle dependencies
- Copied app to server and ran it as a systemd service
- Verified app via curl/browser

## Challenges faced & fixes
- SSH access blocked by firewall → allowed port 22 from my IP
- App port not reachable → opened app port in cloud firewall
- Service failed on reboot → created systemd unit and enabled it

## Files in this folder
See: [`files.md`](../docs/files.md)

## Commands used
See: [`../logs/commands.md`](../logs/commands.md)

## Next improvements (optional)
- Add Nginx reverse proxy + HTTPS (Let's Encrypt)
- Use Ansible for repeatable provisioning
- Containerize the app with Docker
