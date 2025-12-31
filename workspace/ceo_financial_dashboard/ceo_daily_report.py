"""
DM Global Tur - CEO Daily Report Automation
- Fetches data from Supabase and Stripe
- Processes insights with Gemini 1.5 Flash
- Sends executive summary via Email (Resend/SendGrid) and/or Slack/WhatsApp webhook
- Scheduled to run daily at 08:00 UTC
"""
import os
import datetime
import stripe
from supabase import create_client, Client
import google.generativeai as genai
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv

load_dotenv()

# --- ENV VARS ---
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
WHATSAPP_WEBHOOK_URL = os.getenv('WHATSAPP_WEBHOOK_URL')
CEO_EMAILS = os.getenv('CEO_EMAILS', '').split(',')

# --- INIT CLIENTS ---
stripe.api_key = STRIPE_API_KEY
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# --- TIME WINDOW ---
now = datetime.datetime.utcnow()
yesterday = now - datetime.timedelta(days=1)

# --- DATA INGESTION ---
def fetch_supabase_data():
    # Nuevos usuarios
    users = supabase.table('users').select('*').gte('created_at', yesterday.isoformat()).execute().data
    # Carritos abandonados
    abandoned = supabase.table('checkouts').select('*').eq('completed', False).gte('created_at', yesterday.isoformat()).execute().data
    # Carritos recuperados
    recovered = supabase.table('checkouts').select('*').eq('completed', True).gte('recovered_at', yesterday.isoformat()).execute().data
    # Engagement: usuarios activos (ejemplo: logins en las últimas 24h)
    engagement = supabase.table('user_activity').select('*').gte('timestamp', yesterday.isoformat()).execute().data
    # Churn: usuarios que cancelaron en las últimas 24h
    churned = supabase.table('users').select('*').eq('status', 'cancelled').gte('updated_at', yesterday.isoformat()).execute().data
    return users, abandoned, recovered, engagement, churned

def fetch_stripe_data():
    # Ingresos del día
    payments = stripe.PaymentIntent.list(created={
        'gte': int(yesterday.timestamp()),
        'lte': int(now.timestamp())
    }, limit=100)
    total_revenue = sum([p['amount_received']/100 for p in payments if p['status']=='succeeded'])
    # Nuevas suscripciones por Tier
    subscriptions = stripe.Subscription.list(created={
        'gte': int(yesterday.timestamp()),
        'lte': int(now.timestamp())
    }, limit=100)
    tier_counts = {'Tier 1': 0, 'Tier 2': 0, 'Tier 3': 0}
    for sub in subscriptions:
        plan = sub['items']['data'][0]['plan']['nickname']
        if plan in tier_counts:
            tier_counts[plan] += 1
    # Alipay vs Tarjeta
    alipay_success = 0
    card_success = 0
    for p in payments:
        if p['status']=='succeeded':
            if p['payment_method_types'][0] == 'alipay':
                alipay_success += 1
            elif p['payment_method_types'][0] == 'card':
                card_success += 1
    alipay_health = 'OK' if alipay_success > 0 else 'ISSUE'
    # ARPU: Average Revenue Per User (día)
    arpu = total_revenue / max(1, len(subscriptions))
    return total_revenue, tier_counts, alipay_success, card_success, alipay_health, arpu

def compute_metrics(users, abandoned, recovered, total_revenue, tier_counts, alipay_success, card_success, alipay_health):
    recovery_rate = (len(recovered) / (len(abandoned) + len(recovered))) * 100 if (len(abandoned) + len(recovered)) > 0 else 0
    churn_rate = (len(churned) / max(1, len(users) + len(churned))) * 100
    engagement_rate = (len(engagement) / max(1, len(users))) * 100
    return {
        'total_revenue': total_revenue,
        'tier_counts': tier_counts,
        'new_users': len(users),
        'recovery_rate': recovery_rate,
        'alipay_health': alipay_health,
        'alipay_success': alipay_success,
        'card_success': card_success,
        'churn_rate': churn_rate,
        'arpu': arpu,
        'engagement_rate': engagement_rate
    }

def generate_insights(metrics):
    prompt = f"""
Eres el Analista Financiero de DM Global Tur. Resume los datos del día:
- Ingresos totales: ${metrics['total_revenue']:.2f}
- Nuevas suscripciones: {metrics['tier_counts']}
- Nuevos usuarios: {metrics['new_users']}
- Tasa de recuperación de carritos: {metrics['recovery_rate']:.2f}%
- Estado Alipay: {metrics['alipay_health']} (Alipay: {metrics['alipay_success']}, Tarjeta: {metrics['card_success']})

Destaca el crecimiento de MRR, identifica si hay algún cuello de botella en los pagos de Alipay y redacta una breve recomendación estratégica para los fundadores.
"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def format_html_report(metrics, insights):
        return f'''
        <html>
        <head>
        <style>
            body {{ background: #18181a; color: #fff; font-family: Arial, sans-serif; }}
            .card {{ background: #232326; border-radius: 12px; padding: 24px; margin: 16px 0; box-shadow: 0 2px 8px #0003; }}
            .gold {{ color: #bfa14a; }}
            .red {{ color: #e53935; }}
            h1 {{ color: #bfa14a; }}
            h2 {{ color: #e53935; }}
            .metric {{ font-size: 1.2em; margin: 8px 0; }}
        </style>
        </head>
        <body>
            <h1 class="gold">DM Global Tur - Executive Daily Report</h1>
            <div class="card">
                <div class="metric gold">💰 Ingresos Totales: <b>${metrics['total_revenue']:.2f}</b></div>
                <div class="metric">📈 Nuevas Suscripciones: {metrics['tier_counts']}</div>
                <div class="metric">🛒 Tasa de Recuperación de Carritos: <b>{metrics['recovery_rate']:.2f}%</b></div>
                <div class="metric">📉 Churn Rate: <b>{metrics['churn_rate']:.2f}%</b></div>
                <div class="metric">💸 ARPU: <b>${metrics['arpu']:.2f}</b></div>
                <div class="metric">🔥 Engagement Rate: <b>{metrics['engagement_rate']:.2f}%</b></div>
                <div class="metric">🇨🇳 Estado Alipay: <span class="{'gold' if metrics['alipay_health']=='OK' else 'red'}">{metrics['alipay_health']}</span></div>
                <div class="metric">🤖 IA Insights: <i>{insights}</i></div>
            </div>
        </body>
        </html>
        '''

def send_ceo_report(html):
    # Email via SendGrid (fallback to SMTP demo)
    if SENDGRID_API_KEY:
        import sendgrid
        from sendgrid.helpers.mail import Mail
        sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        for email in CEO_EMAILS:
            message = Mail(
                from_email='ceo-report@dmglobaltur.com',
                to_emails=email,
                subject='[DM Global Tur] Executive Daily Report',
                html_content=html
            )
            sg.send(message)
    # Resend API (if configured)
    elif RESEND_API_KEY:
        for email in CEO_EMAILS:
            requests.post(
                'https://api.resend.com/emails',
                headers={'Authorization': f'Bearer {RESEND_API_KEY}'},
                json={
                    'from': 'ceo-report@dmglobaltur.com',
                    'to': email,
                    'subject': '[DM Global Tur] Executive Daily Report',
                    'html': html
                }
            )
    # Slack/WhatsApp webhook
    if SLACK_WEBHOOK_URL:
        requests.post(SLACK_WEBHOOK_URL, json={'text': html})
    if WHATSAPP_WEBHOOK_URL:
        requests.post(WHATSAPP_WEBHOOK_URL, json={'text': html})

def main():
    users, abandoned, recovered, engagement, churned = fetch_supabase_data()
    total_revenue, tier_counts, alipay_success, card_success, alipay_health, arpu = fetch_stripe_data()
    metrics = compute_metrics(users, abandoned, recovered, total_revenue, tier_counts, alipay_success, card_success, alipay_health)
    metrics['arpu'] = arpu
    metrics['churn_rate'] = (len(churned) / max(1, len(users) + len(churned))) * 100
    metrics['engagement_rate'] = (len(engagement) / max(1, len(users))) * 100
    insights = generate_insights(metrics)
    html = format_html_report(metrics, insights)
    send_ceo_report(html)

if __name__ == '__main__':
    main()
