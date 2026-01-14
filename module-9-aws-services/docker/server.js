const http = require("http");

const port = process.env.PORT || 3000;
const message = process.env.MESSAGE || "Module 9 CI/CD Pipeline Successful 🚀";

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end(message);
});

server.listen(port, () => console.log(`App running on port ${port}`));
