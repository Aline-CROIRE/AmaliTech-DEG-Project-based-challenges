const validatePaymentBody = (req, res, next) => {
  const { amount, currency } = req.body;

  if (amount === undefined || typeof amount !== 'number' || amount <= 0) {
    return res.status(422).json({ error: 'Invalid amount. Must be a positive number.' });
  }

  if (!currency || typeof currency !== 'string' || currency.length !== 3) {
    return res.status(422).json({ error: 'Invalid currency. Must be a 3-letter ISO code (e.g., GHS).' });
  }

  next();
};

module.exports = validatePaymentBody;