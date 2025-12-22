const http = require('http');

const PORT = 3000;

http.createServer((req, res) => {
  res.end('Module 8 CI/CD Pipeline Successful 🚀');
}).listen(PORT, () => {
  console.log(`App running on port ${PORT}`);
});
