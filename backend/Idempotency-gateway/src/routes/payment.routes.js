const express = require('express');
const router = express.Router();
const { processPayment } = require('../controllers/payment.controller');
const idempotencyMiddleware = require('../middleware/idempotency.middleware');
const validatePaymentBody = require('../middleware/validation.middleware');

/**
 * @openapi
 * /process-payment:
 *   post:
 *     summary: Process a payment
 *     description: Validates payload, checks idempotency, and processes payment.
 *     parameters:
 *       - in: header
 *         name: Idempotency-Key
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - amount
 *               - currency
 *             properties:
 *               amount:
 *                 type: number
 *                 example: 100
 *               currency:
 *                 type: string
 *                 example: FRW
 *     responses:
 *       200:
 *         description: Success
 *       409:
 *         description: Conflict (Key reused with different body)
 *       422:
 *         description: Unprocessable Entity (Validation failed)
 */
router.post('/process-payment', validatePaymentBody, idempotencyMiddleware, processPayment);

module.exports = router;