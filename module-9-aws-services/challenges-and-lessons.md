# Challenges Faced & Lessons Learned

## SSH Authentication Failures
**Problem:** Jenkins SSH failures due to key format and agent issues.
**Solution:** Created a dedicated deployment key and used Jenkins Secret File credentials.
**Lesson:** Always validate SSH manually before automating.

## Docker Socket Permissions
**Problem:** Jenkins could not access Docker daemon.
**Solution:** Installed Docker client inside Jenkins container and aligned permissions.
**Lesson:** Jenkins containers need explicit Docker access.

## AWS CLI Confusion
**Problem:** AWS CLI worked locally but not in Jenkins.
**Solution:** Installed AWS CLI inside Jenkins container and used Jenkins credentials.
**Lesson:** Jenkins runs in an isolated environment.

## Smoke Test Failures
**Problem:** App was running but not returning expected output.
**Solution:** Improved retry logic and response validation.
**Lesson:** Deployment success ≠ application health.