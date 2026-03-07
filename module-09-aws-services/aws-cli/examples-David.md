# AWS CLI Examples

## Configure
```bash
aws configure
aws sts get-caller-identity
```

## EC2
```bash
aws ec2 describe-instances
aws ec2 create-key-pair --key-name mykey --query 'KeyMaterial' --output text > mykey.pem
chmod 400 mykey.pem
```

## ECR
```bash
aws ecr create-repository --repository-name myapp
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
docker tag myapp:local <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/myapp:v1
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/myapp:v1
```
