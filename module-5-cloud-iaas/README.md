# Module 5 – Cloud & Infrastructure as a Service (IaaS)

This project demonstrates deploying a Java Spring Boot application on a cloud-based Linux server using Infrastructure as a Service principles.

## Technologies
- DigitalOcean
- Ubuntu Linux
- Java 17
- Gradle (Wrapper recommended)
- Spring Boot

## What Was Done
- Provisioned a cloud server
- Connected via SSH
- Installed Java 17
- Built the application using Gradle
- Created a non-root Linux user
- Ran the application on port 8080
- Verified deployment using curl

## Screenshots
Add your evidence screenshots into `screenshots/` and (optionally) embed them here.

## Notes about Gradle Wrapper
This package includes a *placeholder* `gradlew` and wrapper config to keep the portfolio structure consistent.
If you want the wrapper fully functional, run this once on your laptop (with Gradle installed):

```bash
cd java-react-example
gradle wrapper
```

Then commit the generated `gradlew`, `gradlew.bat`, `gradle/wrapper/gradle-wrapper.jar`, and updated properties file.


Step-by-Step Implementation (Full Commands & Code)
1. Provision Cloud VM (IaaS)

Create a cloud virtual machine (e.g. DigitalOcean, AWS EC2, Azure VM):

OS: Ubuntu

SSH access enabled

Public IP address assigned

Evidence: screenshots/digitalocean-droplet-created.png.png

2. SSH into the Server
ssh root@<SERVER_PUBLIC_IP>


Or using SSH key:

ssh -i ~/.ssh/id_ed25519 root@<SERVER_PUBLIC_IP>

3. Update the System
apt update -y
apt upgrade -y

4. Install Java (OpenJDK 17)
apt install -y openjdk-17-jdk
java -version


Evidence: screenshots/java-and-gradle-installed.png.png

5. Install Gradle
apt install -y gradle
gradle -v

6. Create a Non-Root User (Best Practice)
adduser appuser
usermod -aG sudo appuser
su - appuser


Evidence:
screenshots/non-root-user-created.png.png
screenshots/application-running-as-non-root.png.png

7. Prepare Application Directory
cd ~
mkdir java-react-example
cd java-react-example

Application Configuration & Code
settings.gradle
rootProject.name = 'java-react-example'

build.gradle
plugins {
    id 'java'
    id 'application'
}

group = 'com.coditorium.sandbox'
version = '1.0.0'

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

application {
    mainClass = 'com.coditorium.sandbox.Application'
}

src/main/java/com/coditorium/sandbox/Application.java
package com.coditorium.sandbox;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

src/main/java/com/coditorium/sandbox/HealthController.java
package com.coditorium.sandbox;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

    @GetMapping("/health")
    public String health() {
        return "Application is running successfully";
    }
}

src/main/resources/static/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Module 5 Application</title>
</head>
<body>
    <h1>Java Application Running on Cloud VM</h1>
    <p>Deployed as part of Module 5 – Cloud IaaS</p>
</body>
</html>

Build & Run the Application
8. Build the Application
gradle clean build

9. Run the Application
java -jar build/libs/java-react-example-1.0.0.jar


Evidence: screenshots/application running.png

10. Verify Port 8080
ss -lntp | grep 8080


Evidence: screenshots/port-8080-listening.png.png

11. Open Firewall Port
ufw allow 8080/tcp
ufw reload
ufw status


Ensure the cloud provider firewall also allows inbound TCP 8080.

12. Test the Application

From the server:

curl http://localhost:8080
curl http://localhost:8080/health


From local machine:

curl http://<SERVER_PUBLIC_IP>:8080


Browser:

http://<SERVER_PUBLIC_IP>:8080


Evidence:
screenshots/curl-success.png.png
screenshots/application running.png

Troubleshooting Commands
ps aux | grep java
ss -lntp
journalctl -xe