// Node.js (Express) - User Onboarding Flow
const { createClient } = require('@supabase/supabase-js');
const stripe = require('stripe')(process.env.STRIPE_API_KEY);
const axios = require('axios');

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

async function handleUserSignUp({ user_id, email, company_name, country_code, ip }) {
  // 1. Insertar usuario en tabla users
  const { data: user, error: userError } = await supabase
    .from('users')
    .insert({ id: user_id, email, company_name, country_code, tier_id: 0 })
    .select()
    .single();
  if (userError) throw new Error('Error insertando usuario: ' + userError.message);

  // 2. Crear Customer en Stripe
  let stripeCustomer;
  try {
    stripeCustomer = await stripe.customers.create({ email, name: company_name });
  } catch (err) {
    // Rollback usuario
    await supabase.from('users').delete().eq('id', user_id);
    throw new Error('Error creando cliente en Stripe: ' + err.message);
  }
  // 3. Guardar stripe_customer_id
  await supabase.from('users').update({ stripe_customer_id: stripeCustomer.id }).eq('id', user_id);

  // 4. Llamar a intelligence_engine para Welcome Insight
  try {
    await axios.post(process.env.INTELLIGENCE_ENGINE_URL + '/generate_welcome_insight', {
      user_id,
      country_code,
      ip
    });
  } catch (err) {
    // No es crítico, solo log
    console.error('Error llamando a intelligence_engine:', err.message);
  }

  return { status: 'ok', user_id, stripe_customer_id: stripeCustomer.id };
}

module.exports = handleUserSignUp;
