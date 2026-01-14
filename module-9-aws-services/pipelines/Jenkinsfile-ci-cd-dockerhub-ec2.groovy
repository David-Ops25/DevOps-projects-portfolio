pipeline {
  agent any

  environment {
    IMAGE_NAME = "davidangyu/jenkins-cicd-demo-app"
    IMAGE_TAG  = "${BUILD_NUMBER}"

    APP_HOST   = "51.20.255.131"           // <-- set your app server public IP
    DEPLOY_DIR = "/home/ec2-user/demo2"
    AWS_REGION = "eu-north-1"
  }

  options {
    timestamps()
    disableConcurrentBuilds()
    timeout(time: 30, unit: 'MINUTES')
  }

  stages {
    stage('Checkout') {
      steps {
        git(
          url: 'https://github.com/David-Ops25/DevOps-projects-portfolio.git',
          branch: 'main',
          credentialsId: 'github-pat'
        )
      }
    }

    stage('Build Image') {
      steps {
        dir('docker') {
          sh '''
            set -euo pipefail
            echo "Building ${IMAGE_NAME}:${IMAGE_TAG}"
            docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
          '''
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            set -euo pipefail
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push ${IMAGE_NAME}:${IMAGE_TAG}
            docker logout
          '''
        }
      }
    }

    stage('Deploy to EC2 (docker compose)') {
      steps {
        withCredentials([file(credentialsId: 'jenkins-deploy-key', variable: 'KEYFILE')]) {
          sh '''
            set -euo pipefail
            chmod 400 "$KEYFILE"

            ssh -i "$KEYFILE" -o StrictHostKeyChecking=no ec2-user@$APP_HOST \
              "DEPLOY_DIR='$DEPLOY_DIR' IMAGE='${IMAGE_NAME}:${IMAGE_TAG}' bash -s" <<'REMOTE'
              set -euo pipefail
              mkdir -p "$DEPLOY_DIR"
              cd "$DEPLOY_DIR"

              cat > docker-compose.yml <<YML
services:
  mongodb:
    image: mongo:6
    container_name: mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongo_data:/data/db
    networks:
      - demo2-net

  mongo-express:
    image: mongo-express:1.0.2
    container_name: mongo-express
    restart: unless-stopped
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: password
      ME_CONFIG_MONGODB_SERVER: mongodb
    depends_on:
      - mongodb
    networks:
      - demo2-net

  app:
    image: ${IMAGE}
    container_name: demo2-app
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      MESSAGE: "Module 9 CI/CD Pipeline Successful 🚀"
    depends_on:
      - mongodb
    networks:
      - demo2-net

volumes:
  mongo_data:

networks:
  demo2-net:
YML

              docker compose pull
              docker compose up -d
              docker ps
REMOTE
          '''
        }
      }
    }

    stage('Smoke test') {
      steps {
        withCredentials([file(credentialsId: 'jenkins-deploy-key', variable: 'KEYFILE')]) {
          sh '''
            set -euo pipefail
            chmod 400 "$KEYFILE"

            ssh -i "$KEYFILE" -o StrictHostKeyChecking=no ec2-user@$APP_HOST 'bash -s' <<'REMOTE'
              set -euo pipefail

              for i in $(seq 1 20); do
                echo "Smoke test attempt $i..."
                if curl -fsS http://localhost:3000/ -o /tmp/app_out.txt; then
                  echo "Response:"
                  cat /tmp/app_out.txt
                  echo

                  if grep -qi "Module 9 CI/CD Pipeline Successful" /tmp/app_out.txt; then
                    echo "Smoke test OK"
                    exit 0
                  fi
                fi
                sleep 2
              done

              echo "Smoke test FAILED. Recent logs:"
              docker logs --tail 100 demo2-app || true
              exit 1
REMOTE
          '''
        }
      }
    }

    stage('AWS identity (Jenkins)') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-jenkins']]) {
          sh '''
            set -euo pipefail
            aws sts get-caller-identity
          '''
        }
      }
    }
  }
}
