pipeline {
  agent any

  environment {
    APP_HOST   = "51.20.255.131"
    DEPLOY_DIR = "/home/ec2-user/demo2"
    APP_IMAGE  = "davidangyu/jenkins-cicd-demo-app:latest"
  }

  stages {
    stage('Deploy latest to EC2') {
      steps {
        withCredentials([file(credentialsId: 'jenkins-deploy-key', variable: 'KEYFILE')]) {
          sh '''
            set -e
            chmod 400 "$KEYFILE"
            ssh -i "$KEYFILE" -o StrictHostKeyChecking=no ec2-user@$APP_HOST \
              "DEPLOY_DIR='$DEPLOY_DIR' IMAGE='$APP_IMAGE' bash -s" <<'REMOTE'
              set -e
              mkdir -p "$DEPLOY_DIR"
              cd "$DEPLOY_DIR"
              # assumes docker-compose.yml already exists in DEPLOY_DIR
              docker compose pull
              docker compose up -d
              docker ps
REMOTE
          '''
        }
      }
    }
  }
}
