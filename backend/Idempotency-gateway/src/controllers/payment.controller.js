const storage = require('../services/storage.service');

const processPayment = async (req, res) => {
  const key = req.headers['idempotency-key'];

  await new Promise((resolve) => setTimeout(resolve, 2000));

  const responseBody = {
    status: 'success',
    message: `Charged ${req.body.amount} ${req.body.currency}`,
  };

  storage.set(key, {
    status: 'COMPLETED',
    statusCode: 200,
    responseBody: responseBody,
    requestBody: req.body
  });

  res.status(200).json(responseBody);
};

module.exports = { processPayment };