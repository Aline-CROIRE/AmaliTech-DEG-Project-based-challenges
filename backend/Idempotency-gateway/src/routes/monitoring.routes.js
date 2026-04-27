const express = require('express');
const router = express.Router();
const logger = require('../services/logger.service');

/**
 * @openapi
 * /audit-logs:
 *   get:
 *     tags:
 *       - System Monitoring
 *     summary: Retrieve system audit trails
 *     description: Returns a complete history of idempotency events, including requests, successes, and conflicts.
 *     responses:
 *       200:
 *         description: A list of audit log entries.
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 */
router.get('/audit-logs', (req, res) => {
  res.status(200).json(logger.getLogs());
});

/**
 * @openapi
 * /health:
 *   get:
 *     tags:
 *       - System Monitoring
 *     summary: Service health check
 *     description: Simple endpoint to verify the gateway is operational.
 *     responses:
 *       200:
 *         description: Returns status UP
 */
router.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP' });
});

module.exports = router;