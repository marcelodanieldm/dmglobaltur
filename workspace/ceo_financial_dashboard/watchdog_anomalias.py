"""
DM Global Tur - Watchdog de Anomalías
- Monitorea ventas, pagos y consumo de IA
- Alerta inmediata a CEO y QA ante anomalías críticas
"""
import os
import datetime
import asyncio
import stripe
from supabase import create_client, Client
import google.generativeai as genai
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
CEO_EMAILS = os.getenv('CEO_EMAILS', '').split(',')
QA_EMAIL = os.getenv('QA_EMAIL', 'daniel@dmglobaltur.com')

stripe.api_key = STRIPE_API_KEY
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)

async def fetch_sales_last_6h():
    now = datetime.datetime.utcnow()
    since = now - datetime.timedelta(hours=6)
    payments = stripe.PaymentIntent.list(created={
        'gte': int(since.timestamp()),
        'lte': int(now.timestamp())
    }, limit=100)
    revenue = sum([p['amount_received']/100 for p in payments if p['status']=='succeeded'])
    return revenue

async def fetch_sales_historic():
    now = datetime.datetime.utcnow()
    since = now - datetime.timedelta(days=7)
    payments = stripe.PaymentIntent.list(created={
        'gte': int(since.timestamp()),
        'lte': int(now.timestamp())
    }, limit=1000)
    # Agrupa por bloques de 6h
    buckets = {}
    for p in payments:
        if p['status']=='succeeded':
            t = datetime.datetime.utcfromtimestamp(p['created'])
            bucket = t.replace(minute=0, second=0, microsecond=0, hour=(t.hour//6)*6)
            buckets.setdefault(bucket, 0)
            buckets[bucket] += p['amount_received']/100
    return buckets

async def fetch_payment_failures():
    events = stripe.Event.list(type='payment_intent_payment_failed', limit=10)
    failures = [e for e in events]
    return failures

async def fetch_gemini_token_usage():
    # Simula consulta a tabla de logs de consumo de tokens
    logs = supabase.table('gemini_usage').select('*').order('timestamp', desc=True).limit(7).execute().data
    today = logs[0]['tokens'] if logs else 0
    avg = sum([l['tokens'] for l in logs[1:]]) / max(1, len(logs)-1) if len(logs) > 1 else 0
    return today, avg

async def fetch_last_error_logs():
    logs = supabase.table('error_logs').select('*').order('timestamp', desc=True).limit(50).execute().data
    return '\n'.join([l['message'] for l in logs])

def send_critical_alert(subject, message):
    # Slack
    if SLACK_WEBHOOK_URL:
        requests.post(SLACK_WEBHOOK_URL, json={'text': f'*{subject}*\n{message}'})
    # Email (SendGrid/SMTP demo)
    for email in CEO_EMAILS + [QA_EMAIL]:
        requests.post(
            'https://api.resend.com/emails',
            headers={'Authorization': f'Bearer {os.getenv("RESEND_API_KEY")}'},
            json={
                'from': 'alert@dmglobaltur.com',
                'to': email,
                'subject': subject,
                'html': f'<b>{subject}</b><br>{message}'
            }
        )

async def main():
    # 1. Caída de ventas
    revenue_6h = await fetch_sales_last_6h()
    historic = await fetch_sales_historic()
    historic_nonzero = any(v > 0 for v in historic.values())
    if revenue_6h == 0 and historic_nonzero:
        logs = await fetch_last_error_logs()
        prompt = f"Analiza estos logs y explica por qué no hubo ventas en las últimas 6h.\n{logs}"
        model = genai.GenerativeModel('gemini-1.5-flash')
        explanation = model.generate_content(prompt).text
        send_critical_alert('URGENTE: Caída de Ventas', f'Ingresos 6h: $0. Explicación IA: {explanation}')
    # 2. Fallo de pasarela
    failures = await fetch_payment_failures()
    if len(failures) >= 3:
        logs = await fetch_last_error_logs()
        prompt = f"Analiza estos logs y explica la causa de los fallos de pago.\n{logs}"
        model = genai.GenerativeModel('gemini-1.5-flash')
        explanation = model.generate_content(prompt).text
        send_critical_alert('URGENTE: Fallo de Pasarela de Pago', f'Errores Stripe/Alipay: {len(failures)}. Explicación IA: {explanation}')
    # 3. Costo IA anómalo
    today, avg = await fetch_gemini_token_usage()
    if avg > 0 and today > avg * 1.5:
        logs = await fetch_last_error_logs()
        prompt = f"Analiza estos logs y explica el aumento de consumo de tokens Gemini.\n{logs}"
        model = genai.GenerativeModel('gemini-1.5-flash')
        explanation = model.generate_content(prompt).text
        send_critical_alert('URGENTE: Costo de IA Anómalo', f'Consumo tokens hoy: {today}, promedio: {avg:.0f}. Explicación IA: {explanation}')

if __name__ == '__main__':
    asyncio.run(main())
