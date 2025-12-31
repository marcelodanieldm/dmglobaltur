import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
DB_URL = os.getenv('DATABASE_URL')  # Formato: postgres://user:pass@host:port/dbname

# --- Slack Notifier ---
def send_slack_alert(channel, message):
    if SLACK_WEBHOOK_URL:
        # Slack webhooks do not use channel param, but can be extended for multiple URLs
        requests.post(SLACK_WEBHOOK_URL, json={'text': message})

# --- DB Logger ---
def log_system_health(user_id, source, event, message):
    if not DB_URL:
        print(f"[LOG] {user_id} | {source} | {event} | {message}")
        return
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO system_health_logs (user_id, source, event, message)
            VALUES (%s, %s, %s, %s)
        ''', (user_id, source, event, message))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] {e}")
