# Commands Used

> Add your real command history here. The blocks below are safe templates.

## Create droplet and secure SSH
```bash
ssh root@<DROPLET_IP>
adduser appuser
usermod -aG sudo appuser
mkdir -p /home/appuser/.ssh
# copy your public key
ufw allow OpenSSH
ufw enable
```

## Install Java/Gradle and deploy
```bash
sudo apt update
sudo apt install -y openjdk-17-jre
# copy artifact
scp build/libs/app.jar appuser@<DROPLET_IP>:/opt/myapp/app.jar
sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl start myapp
curl http://localhost:<APP_PORT>
```
