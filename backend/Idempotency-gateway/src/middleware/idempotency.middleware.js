const storage = require('../services/storage.service');

const idempotencyMiddleware = (req, res, next) => {
  const key = req.headers['idempotency-key'];

  if (!key) {
    return res.status(400).json({ error: 'Idempotency-Key header is required' });
  }

  if (storage.has(key)) {
    const cachedRecord = storage.get(key);

    const incomingBody = JSON.stringify(req.body);
    const storedBody = JSON.stringify(cachedRecord.requestBody);

    if (incomingBody !== storedBody) {
      return res.status(409).json({
        error: "Idempotency key already used for a different request body."
      });
    }

    if (cachedRecord.status === 'COMPLETED') {
      res.set('X-Cache-Hit', 'true');
      return res.status(cachedRecord.statusCode).json(cachedRecord.responseBody);
    }
  }

  next();
};

module.exports = idempotencyMiddleware;