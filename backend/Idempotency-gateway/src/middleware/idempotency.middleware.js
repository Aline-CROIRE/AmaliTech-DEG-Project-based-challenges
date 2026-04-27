const storage = require('../services/storage.service');
const logger = require('../services/logger.service');

const idempotencyMiddleware = async (req, res, next) => {
  const key = req.headers['idempotency-key'];

  if (!key) {
    return res.status(400).json({ error: 'Idempotency-Key header is required' });
  }

  if (storage.has(key)) {
    let cachedRecord = storage.get(key);

    const incomingBody = JSON.stringify(req.body);
    const storedBody = JSON.stringify(cachedRecord.requestBody);

    if (incomingBody !== storedBody) {
      logger.log({
        key,
        action: 'CONFLICT_DETECTED',
        payload: req.body,
        error: 'Body mismatch'
      });
      return res.status(409).json({
        error: "Idempotency key already used for a different request body."
      });
    }

    if (cachedRecord.status === 'PROCESSING') {
      logger.log({ key, action: 'CONCURRENT_WAIT', payload: req.body });
      cachedRecord = await storage.waitForCompletion(key);
    }

    if (cachedRecord.status === 'COMPLETED') {
      logger.log({ key, action: 'CACHE_HIT', payload: req.body });
      res.set('X-Cache-Hit', 'true');
      res.set('X-Idempotency-Expiration', new Date(cachedRecord.expiresAt).toISOString());
      return res.status(cachedRecord.statusCode).json(cachedRecord.responseBody);
    }
  }

  logger.log({ key, action: 'REQUEST_RECEIVED', payload: req.body });

  storage.set(key, {
    status: 'PROCESSING',
    requestBody: req.body
  });

  next();
};

module.exports = idempotencyMiddleware;