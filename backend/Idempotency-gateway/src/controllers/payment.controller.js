const storage = require('../services/storage.service');
const logger = require('../services/logger.service');

const processPayment = async (req, res) => {
  const key = req.headers['idempotency-key'];

  await new Promise((resolve) => setTimeout(resolve, 2000));

  const responseBody = {
    status: 'success',
    message: `Charged ${req.body.amount} ${req.body.currency}`,
  };

  const record = {
    status: 'COMPLETED',
    statusCode: 200,
    responseBody: responseBody,
    requestBody: req.body
  };

  storage.set(key, record);

  const savedRecord = storage.get(key);

  logger.log({
    key,
    action: 'PAYMENT_PROCESSED',
    payload: req.body,
    response: responseBody
  });

  res.set('X-Idempotency-Expiration', new Date(savedRecord.expiresAt).toISOString());
  res.status(200).json(responseBody);
};

module.exports = { processPayment };