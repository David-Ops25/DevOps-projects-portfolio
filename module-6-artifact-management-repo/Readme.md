# Module 6 – Artifact Management with Nexus Repository

## Overview
This module demonstrates a complete, hands-on implementation of artifact management using **Sonatype Nexus Repository (Community Edition)** integrated with **Gradle** on a Linux server.

The project shows how a Java application is built and published to a self-hosted Nexus Repository running on Ubuntu 24.04, validating a real-world DevOps artifact lifecycle.

## Objectives
- Install and access Nexus Repository Manager
- Configure Maven proxy, hosted, and group repositories
- Build a Java application using Gradle
- Publish release artifacts to Nexus (maven-releases)
- Verify artifacts through the Nexus UI

## Architecture
Developer / CI (Gradle)
→ Build Java application
→ Publish artifact (JAR)
→ Nexus Repository (Hosted Maven Repo)
→ Artifact available for downstream services

## Repository Structure
module-6-nexus-repository/
├── gradle-nexus-demo/
│   ├── build.gradle
│   ├── settings.gradle
│   └── src/main/java/App.java
├── screenshots/
│   └── *.png
└── README.md

## DevOps Perspective
This module focuses on platform enablement rather than manual support. Nexus provides a central, versioned, and auditable artifact store, reducing risk and improving delivery reliability.

## Status
Completed and verified.