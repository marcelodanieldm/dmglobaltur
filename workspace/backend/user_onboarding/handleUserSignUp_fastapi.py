# FastAPI - User Onboarding Flow
import os
from fastapi import HTTPException
from supabase import create_client, Client
import stripe
import requests

supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
stripe.api_key = os.getenv('STRIPE_API_KEY')

async def handle_user_signup(user_id, email, company_name, country_code, ip):
    # 1. Insertar usuario en tabla users
    resp = supabase.table('users').insert({
        'id': user_id,
        'email': email,
        'company_name': company_name,
        'country_code': country_code,
        'tier_id': 0
    }).execute()
    if resp.error:
        raise HTTPException(status_code=500, detail='Error insertando usuario: ' + resp.error.message)

    # 2. Crear Customer en Stripe
    try:
        customer = stripe.Customer.create(email=email, name=company_name)
    except Exception as e:
        supabase.table('users').delete().eq('id', user_id).execute()
        raise HTTPException(status_code=500, detail='Error creando cliente en Stripe: ' + str(e))
    supabase.table('users').update({'stripe_customer_id': customer['id']}).eq('id', user_id).execute()

    # 3. Llamar a intelligence_engine para Welcome Insight
    try:
        requests.post(os.getenv('INTELLIGENCE_ENGINE_URL') + '/generate_welcome_insight',
                      json={'user_id': user_id, 'country_code': country_code, 'ip': ip})
    except Exception as e:
        print('Error llamando a intelligence_engine:', e)

    return {'status': 'ok', 'user_id': user_id, 'stripe_customer_id': customer['id']}
