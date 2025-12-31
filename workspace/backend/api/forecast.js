// Express API for protected forecast endpoints
const express = require('express');
const permissionMiddleware = require('../middleware/permission_middleware');
const router = express.Router();

// Dummy insights for demo
const INSIGHTS = {
  vibe: { main: 'Tus clientes buscan experiencias exclusivas.', sentiment: 0.7, details: { trend: 'Luxury', score: 0.7 } },
  scarcity: { main: 'Alta demanda en fechas clave.', sentiment: 0.8, details: { sold_out: true, next_window: '2026-01-10' } },
  reputation: { main: 'Riesgo reputacional bajo.', sentiment: 0.95, details: { reviews: 'Positivas', alerts: [] } }
};

router.use(permissionMiddleware);

router.get('/insights', (req, res) => {
  // All tiers can access this endpoint
  res.json(INSIGHTS);
});

router.get('/dragon/secret', (req, res) => {
  // Only Dragon Emperor tier
  if (req.userProfile.tier !== 'Dragon Emperor') {
    return res.status(403).json({ error: 'Upgrade required', upgrade_url: process.env.STRIPE_UPGRADE_URL });
  }
  res.json({ secret: 'Solo para Dragon Emperor' });
});

module.exports = router;
