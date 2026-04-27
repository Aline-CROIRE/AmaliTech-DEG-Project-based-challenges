const express = require('express');
const router = express.Router();
const { processPayment } = require('../controllers/payment.controller');
const idempotencyMiddleware = require('../middleware/idempotency.middleware');
const validatePaymentBody = require('../middleware/validation.middleware');

/**
 * @openapi
 * /process-payment:
 *   post:
 *     tags:
 *       - Payment Processing
 *     summary: Process a secure payment
 *     description: Validates the payload and ensures the payment is processed exactly once using the Idempotency-Key.
 *     parameters:
 *       - $ref: '#/components/parameters/IdempotencyKey'
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/PaymentRequest'
 *     responses:
 *       200:
 *         description: Payment successful (or retrieved from cache)
 *         headers:
 *           X-Cache-Hit:
 *             schema: { type: 'boolean' }
 *             description: Indicates if the response was served from the idempotency cache.
 *           X-Idempotency-Expiration:
 *             schema: { type: 'string', format: 'date-time' }
 *             description: The timestamp when this idempotency key will expire.
 *       400:
 *         description: Bad Request (Missing headers or malformed JSON)
 *       409:
 *         description: Conflict (Key reused with different body)
 *       422:
 *         description: Validation Error (Invalid amount or currency)
 */
router.post('/process-payment', validatePaymentBody, idempotencyMiddleware, processPayment);

module.exports = router;