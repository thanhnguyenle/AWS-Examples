// app.js - Simple Node.js application
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

// Version tracking
const VERSION = process.env.APP_VERSION || 'v1.0';
const DEPLOYMENT_STRATEGY = process.env.DEPLOYMENT_STRATEGY || 'unknown';

app.get('/', (req, res) => {
  res.send(`
    <html>
      <head>
        <title>Test App ${VERSION}</title>
        <style>
          body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
          .version { color: #0066cc; font-size: 24px; }
          .strategy { color: #009900; font-size: 18px; }
          .info { background: #f0f0f0; padding: 20px; margin: 20px; border-radius: 5px; }
        </style>
      </head>
      <body>
        <h1>Elastic Beanstalk Test Application</h1>
        <div class="version">Version: ${VERSION}</div>
        <div class="strategy">Deployment Strategy: ${DEPLOYMENT_STRATEGY}</div>
        <div class="info">
          <h3>Server Info:</h3>
          <p>Hostname: ${require('os').hostname()}</p>
          <p>Platform: ${require('os').platform()}</p>
          <p>Uptime: ${Math.floor(process.uptime())} seconds</p>
          <p>Memory Usage: ${Math.round(process.memoryUsage().heapUsed / 1024 / 1024)} MB</p>
        </div>
        <div class="info">
          <h3>Test Different Versions:</h3>
          <p>Change APP_VERSION environment variable to see version updates</p>
          <p>Current Time: ${new Date().toISOString()}</p>
        </div>
      </body>
    </html>
  `);
});

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    version: VERSION,
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

app.get('/version', (req, res) => {
  res.json({
    version: VERSION,
    deployment_strategy: DEPLOYMENT_STRATEGY,
    node_version: process.version
  });
});

app.listen(port, () => {
  console.log(`App ${VERSION} running on port ${port}`);
  console.log(`Deployment strategy: ${DEPLOYMENT_STRATEGY}`);
});