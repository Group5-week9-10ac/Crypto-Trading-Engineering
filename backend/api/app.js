const express = require('express');
const bodyParser = require('body-parser');
const backtestRoutes = require('./routes/backtestRoutes');

const app = express();

app.use(bodyParser.json());
app.use('/api', backtestRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
