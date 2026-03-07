# Commands Used

> Add your real command history here. The blocks below are safe templates.

## Install Nexus (example manual)
```bash
sudo apt update
sudo apt install -y openjdk-17-jre
# download nexus, unzip, configure as service
# open port 8081 in firewall
curl http://localhost:8081
```

## Publish Maven artifact
```bash
mvn -s configs/maven/settings.xml clean deploy -DskipTests
```

## Publish Gradle artifact
```bash
./gradlew clean publish
```
