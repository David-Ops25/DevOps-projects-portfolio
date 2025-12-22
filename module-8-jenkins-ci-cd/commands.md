# Commands used in Module 8

docker run -d --name jenkins ...
docker run -d --name nexus ...
docker login 165.22.127.6:8083
docker build -t module8-demo .
docker push 165.22.127.6:8083/module8-demo
