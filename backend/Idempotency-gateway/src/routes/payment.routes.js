const express = require('express');
const router = express.Router();
const { processPayment } = require('../controllers/payment.controller');
const idempotencyMiddleware = require('../middleware/idempotency.middleware');

/**
 * @openapi
 * /process-payment:
 *   post:
 *     summary: Process a payment
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
 *             properties:
 *               amount:
 *                 type: number
 *               currency:
 *                 type: string
 *     responses:
 *       200:
 *         description: Success
 */
router.post('/process-payment', idempotencyMiddleware, processPayment);

module.exports = router;