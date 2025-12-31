import requests
import os

def send_whatsapp_alert(phone, message):
    # Integración con proveedor WhatsApp Business API (ejemplo: Gupshup, Twilio, 360dialog)
    api_url = os.getenv('WHATSAPP_API_URL')
    api_token = os.getenv('WHATSAPP_API_TOKEN')
    if not api_url or not api_token:
        print('[WhatsApp] Configuración faltante')
        return False
    payload = {
        'to': phone,
        'type': 'text',
        'text': {'body': message}
    }
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    r = requests.post(api_url, json=payload, headers=headers)
    print('[WhatsApp] Status:', r.status_code, r.text)
    return r.status_code == 200
