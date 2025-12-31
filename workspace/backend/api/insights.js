// API endpoint para obtener los últimos insights no abiertos del usuario
const express = require('express');
const { createClient } = require('@supabase/supabase-js');
const router = express.Router();

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

// GET /api/v1/insights/unopened
router.get('/unopened', async (req, res) => {
  const userId = req.headers['x-user-id'];
  if (!userId) return res.status(401).json({ error: 'No user ID' });
  const { data, error } = await supabase
    .from('client_insights')
    .select('*')
    .eq('user_id', userId)
    .eq('was_opened', false)
    .order('delivered_at', { ascending: false })
    .limit(5);
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});


// PATCH /api/v1/insights/mark_opened
router.patch('/mark_opened', async (req, res) => {
  let insight_ids = req.body.insight_ids;
  if (!insight_ids || !Array.isArray(insight_ids)) return res.status(400).json({ error: 'Missing insight_ids' });
  const { error } = await supabase
    .from('client_insights')
    .update({ was_opened: true })
    .in('id', insight_ids);
  if (error) return res.status(500).json({ error: error.message });
  res.json({ status: 'ok' });
});

module.exports = router;
