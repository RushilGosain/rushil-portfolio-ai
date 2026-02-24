const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000',
      changeOrigin: true,
    })
  );
};
```

---

## Fix 4 — Verify Flask is Actually Running

Open your browser and visit:
```
http://localhost:5000/api/health