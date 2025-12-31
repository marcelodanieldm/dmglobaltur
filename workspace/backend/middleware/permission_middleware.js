// Node.js Express middleware for permission and subscription validation
const { createClient } = require('@supabase/supabase-js');
const Redis = require('ioredis');
const STRIPE_UPGRADE_URL = process.env.STRIPE_UPGRADE_URL || 'https://buy.dmglobaltur.com/upgrade';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);
const redis = new Redis(process.env.REDIS_URL);

async function getUserProfile(userId) {
  // Try Redis cache first
  const cached = await redis.get(`user_profile:${userId}`);
  if (cached) return JSON.parse(cached);
  // Fallback to Supabase
  const { data, error } = await supabase
    .from('user_subscriptions')
    .select('*')
    .eq('user_id', userId)
    .single();
  if (error || !data) return null;
  await redis.set(`user_profile:${userId}`, JSON.stringify(data), 'EX', 3600);
  return data;
}

module.exports = async function permissionMiddleware(req, res, next) {
  const userId = req.headers['x-user-id'];
  if (!userId) return res.status(401).json({ error: 'No user ID' });
  const profile = await getUserProfile(userId);
  if (!profile) return res.status(403).json({ error: 'No subscription found', upgrade_url: STRIPE_UPGRADE_URL });
  // Example: block Explorer from Dragon Emperor features
  if (
    req.path.startsWith('/api/v1/forecast/dragon') &&
    profile.tier === 'Explorer'
  ) {
    return res.status(403).json({
      error: 'Upgrade required for Dragon Emperor features',
      upgrade_url: STRIPE_UPGRADE_URL
    });
  }
  req.userProfile = profile;
  next();
};
