const express = require('express');
const swaggerUi = require('swagger-ui-express');
const swaggerSpec = require('./config/swagger');
const paymentRoutes = require('./routes/payment.routes');

const app = express();
const PORT = 3000;

app.use(express.json());

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
app.use('/', paymentRoutes);

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP' });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Swagger docs: http://localhost:3000/api-docs`);
});

module.exports = app;