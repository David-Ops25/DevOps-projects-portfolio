#!/bin/bash
docker build -t module7-dockerfile-demo:1.0 .
docker tag module7-dockerfile-demo:1.0 <NEXUS_IP>:8083/module7-demo:1.0
docker push <NEXUS_IP>:8083/module7-demo:1.0
