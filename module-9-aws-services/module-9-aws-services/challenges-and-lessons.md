# Challenges Faced & Lessons Learned (Professional Summary)

## 1) Jenkins SSH key failures (libcrypto / invalid format)
**Symptoms**
- `Error loading key ... error in libcrypto`
- `Permission denied (publickey)`

**Root cause**
- Key format incompatibility inside Jenkins container / ssh-agent plugin mismatches.

**Fix**
- Generated a dedicated deploy key specifically for Jenkins.
- Stored it as a **Secret file** in Jenkins credentials.
- Used direct `ssh -i "$KEYFILE"` in pipelines.

**Lesson**
Separate “human access” keys from “automation deploy” keys. Validate SSH manually first.

---

## 2) Docker build failed inside Jenkins: Docker not found
**Symptoms**
- `docker: not found` in pipeline.

**Fix**
- Installed Docker CLI inside the Jenkins container (Debian).
- Ensured Jenkins container can access host Docker socket.

**Lesson**
Jenkins in Docker is an isolated runtime; tools must be present inside the container.

---

## 3) Docker socket permission denied
**Symptoms**
- `permission denied while trying to connect to the Docker daemon socket`

**Fix**
- Mapped `/var/run/docker.sock` into Jenkins.
- Started Jenkins container with correct docker group GID (`--group-add <GID>`).

**Lesson**
Docker-in-Docker is different from Docker socket sharing. Permissions must match host.

---

## 4) Smoke test failed even though containers were running
**Symptoms**
- App container up, but pipeline failed at verification stage.

**Fix**
- Added retry loops and printed responses in Jenkins logs.
- Matched expected output string to actual response.

**Lesson**
A green deployment stage isn't enough; always verify via health/smoke tests.

---

## 5) AWS CLI worked locally but not in Jenkins
**Fix**
- Installed AWS CLI v2 inside Jenkins container.
- Used Jenkins credential binding via AWS Credentials plugin.

**Lesson**
Treat Jenkins as its own environment; configure dependencies and credentials explicitly.
