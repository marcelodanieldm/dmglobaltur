import requests
import os
import pandas as pd
from datetime import datetime
from data_ingestion.china_sources import XHS_Scraper

def analyze_inventory_and_generate_insight(inventory_csv_path, city, archetypes, user_id):
    # 1. Leer inventario
    df = pd.read_csv(inventory_csv_path)
    # 2. Obtener tendencias reales de China (mock: XHS_Scraper)
    scraper = XHS_Scraper()
    try:
        china_data = scraper.fetch(city=city, archetypes=archetypes)
    except Exception as e:
        china_data = {'data': 'No se pudo obtener datos de China', 'source': 'XHS_Scraper'}
    # 3. Llamar Gemini 1.5 (API REST o SDK)
    prompt = f"""
Eres un asesor de lujo para nuevos clientes. Analiza el siguiente inventario:
{df.head(10).to_string(index=False)}
Y las tendencias de China hoy:
{china_data['data']}
Género un insight de bienvenida personalizado para el usuario {user_id} en la ciudad {city} y arquetipos {archetypes}.
"""
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        return {'error': 'GEMINI_API_KEY no configurada'}
    # Llamada simple a Gemini 1.5 (mock, reemplazar por SDK real si se desea)
    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
        params={'key': gemini_api_key},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    if response.status_code == 200:
        insight = response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        insight = 'No se pudo generar insight. Error Gemini.'
    # 4. Guardar insight en backend (mock: print)
    print(f"[INSIGHT] {datetime.now()} | {user_id} | {insight}")
    return {'insight': insight}
