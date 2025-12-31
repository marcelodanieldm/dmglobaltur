// Main Express server
const express = require('express');
const cors = require('cors');

const forecastApi = require('./api/forecast');
const insightsApi = require('./api/insights');

const app = express();
app.use(cors());
app.use(express.json());


app.use('/api/v1/forecast', forecastApi);
app.use('/api/v1/insights', insightsApi);

// Static for React/Next.js build (if needed)
// app.use(express.static('../frontend/service_control_panel/out'));

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log('Backend server running on port', PORT);
});
