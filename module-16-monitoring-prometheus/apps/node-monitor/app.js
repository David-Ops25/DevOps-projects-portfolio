const express = require("express");
const client = require("prom-client");

const app = express();
const register = new client.Registry();

client.collectDefaultMetrics({ register });

const httpRequests = new client.Counter({
  name: "app_http_requests_total",
  help: "Total number of HTTP requests",
});

register.registerMetric(httpRequests);

app.get("/", (req, res) => {
  httpRequests.inc();
  res.send("Hello from monitored Node.js app");
});

app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

app.listen(3000, () => {
  console.log("App listening on port 3000");
});
