# Module 8 – overview

Overview

Module 8 focuses on building a real-world CI/CD pipeline using Jenkins, Docker, and Nexus Repository, following industry-standard DevOps practices taught in TechWorld with Nana.

In this module, I designed and implemented a declarative Jenkins pipeline that:

Pulls source code from GitHub

Builds a Docker image

Pushes the image to a private Nexus Docker registry

Uses a Jenkins Shared Library to keep pipelines clean and reusable

Prepares the foundation for Multibranch Pipelines and Webhooks

This module bridges application delivery and automation, showing how DevOps teams ship containerized applications reliably.

 What I Learned in Module 8

How Jenkins works internally (controller, agents, workspaces)

Running Jenkins inside Docker (no local Java installation needed)

Writing Declarative Jenkinsfiles

Connecting Jenkins securely to GitHub using PAT credentials

Building Docker images inside Jenkins

Publishing images to Nexus Docker Registry

Fixing Docker permission issues inside Jenkins containers

Creating and using Jenkins Shared Libraries

Structuring pipelines for scalability and reusability

Understanding Multibranch Pipelines & Webhooks (foundation)

 Architecture (High Level)
GitHub Repo
   ↓
Jenkins Pipeline (Docker container)
   ↓
Docker Build
   ↓
Nexus Docker Registry (Private)
   ↓
(Optional) Deployment

 Folder Structure
module-8-jenkins-ci-cd/
│
├── app/
│   ├── Dockerfile
│   ├── server.js
│   └── package.json
│
├── jenkins/
│   └── Jenkinsfile
│
├── shared-library/
│   └── vars/
│       └── dockerBuildAndPush.groovy
│
├── screenshots/
│   └── (Jenkins UI, pipeline stages, Nexus registry, builds)
│
├── README.md
└── command.md

 Jenkins Setup (Docker)

Jenkins was run inside a Docker container to avoid manual Java installation and to align with modern DevOps practices.

Jenkins UI: http://<droplet-ip>:8080

Nexus UI: http://<droplet-ip>:8081

Nexus Docker Registry: http://<droplet-ip>:8083

 Jenkins Pipeline Stages

The pipeline follows a clear CI/CD flow:

Checkout – Pull source code from GitHub

Test – Placeholder for automated tests

Build Image – Build Docker image

Push to Nexus – Push image to private registry

Deploy (optional) – Future deployment stage

This structure ensures Jenkins shows the classic stage view (Test → Build → Push → Deploy).

 Jenkins Shared Library

A reusable shared library was created to handle Docker build & push logic.

This:

Keeps Jenkinsfiles clean

Promotes DRY (Don’t Repeat Yourself)

Matches real enterprise Jenkins usage

Shared Library Function
dockerBuildAndPush(
  imageName: IMAGE_NAME,
  tag: IMAGE_TAG,
  registry: REGISTRY,
  workDir: 'module-8-jenkins-ci-cd/app'
)

 Credentials & Security

GitHub authentication via Personal Access Token

Docker registry authentication via Jenkins credentials

No secrets hard-coded in Jenkinsfiles

Registry access controlled through Nexus roles

 Multibranch Pipeline & Webhooks (Conceptual Demo)

Although this project uses a single pipeline, the module also covers:

Multibranch Pipeline concepts

GitHub Webhooks for automatic builds

Branch-based CI/CD strategies

This project is fully compatible with conversion to Multibranch Pipelines.

 Outcome

By the end of Module 8, I successfully:

Built a production-style Jenkins pipeline

Automated Docker image creation

Published images to a private registry

Used shared libraries for clean pipelines

Applied CI/CD best practices used in real DevOps teams

 Tech Stack

Jenkins (Dockerized)

Docker

Nexus Repository Manager

GitHub

Groovy (Jenkins DSL)

Linux (Ubuntu)
