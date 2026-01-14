# Dockerfile for a minimal Node.js web service used in the CI/CD demos
# Builds a small container that listens on port 3000
FROM node:20-alpine

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --omit=dev

COPY server.js .

EXPOSE 3000
CMD ["node", "server.js"]
