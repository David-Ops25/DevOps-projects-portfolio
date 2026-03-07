# Commands Used

> Add your real command history here. The blocks below are safe templates.

## Manual deploy on EC2
```bash
ssh -i key.pem ec2-user@<EC2_PUBLIC_IP>
sudo yum update -y
sudo amazon-linux-extras install -y docker
sudo service docker start
sudo usermod -aG docker ec2-user
# pull & run

```

## Jenkins remote deploy idea
```bash
ssh -o StrictHostKeyChecking=no -i key.pem ec2-user@<IP> 'bash -s' < scripts/remote-deploy.sh
```
