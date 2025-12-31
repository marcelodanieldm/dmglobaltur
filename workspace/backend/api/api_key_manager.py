import os
import requests
import random
import string
from supabase import create_client, Client

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_api_key(length=40):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def assign_api_key_to_user(user_id):
    api_key = generate_api_key()
    supabase.table('users').update({'api_key': api_key}).eq('id', user_id).execute()
    return api_key

def get_api_key(user_id):
    res = supabase.table('users').select('api_key').eq('id', user_id).single().execute()
    return res.data['api_key'] if res.data else None
