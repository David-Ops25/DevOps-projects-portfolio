# Nexus Docker Registry Setup

## Steps Performed
1. Deployed Nexus using Docker on cloud VM
2. Exposed ports:
   - 8081 (UI)
   - 8083 (Docker registry)
3. Created Docker hosted repository
4. Created role and user for Docker push/pull
5. Configured Docker insecure registry
6. Pushed image successfully

## Key Commands
docker run -d -p 8081:8081 -p 8083:8083 -v nexus-data:/nexus-data sonatype/nexus3
