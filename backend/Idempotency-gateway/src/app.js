const express = require('express');
const swaggerUi = require('swagger-ui-express');
const swaggerSpec = require('./config/swagger');
const paymentRoutes = require('./routes/payment.routes');
const monitoringRoutes = require('./routes/monitoring.routes');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return res.status(400).json({ error: 'Invalid JSON payload provided.' });
  }
  next();
});

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.use('/', paymentRoutes);
app.use('/', monitoringRoutes);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Swagger docs available at /api-docs`);
});

module.exports = app;