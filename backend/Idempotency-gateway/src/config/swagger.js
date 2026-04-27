const swaggerJsdoc = require('swagger-jsdoc');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'FinSafe Idempotency Gateway API',
      version: '1.1.0',
      description: 'A robust middleware service designed to prevent double-charging by ensuring exactly-once processing of payment requests using unique Idempotency Keys.',
    },
    tags: [
      { name: 'Payment Processing', description: 'Core payment operations' },
      { name: 'System Monitoring', description: 'Health and Audit insights' },
    ],
    components: {
      schemas: {
        PaymentRequest: {
          type: 'object',
          required: ['amount', 'currency'],
          properties: {
            amount: { type: 'number', example: 100 },
            currency: { type: 'string', example: 'FRW' },
          },
        },
      },
      parameters: {
        IdempotencyKey: {
          in: 'header',
          name: 'Idempotency-Key',
          required: true,
          schema: { type: 'string' },
          description: 'Unique string to identify the transaction.',
        },
      },
    },
  },
  apis: ['./src/routes/*.js'],
};

module.exports = swaggerJsdoc(options);