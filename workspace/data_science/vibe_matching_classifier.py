"""
Clasificador de Arquetipos de Turistas de Lujo usando Gemini 1.5 Pro
- Entrada: texto de reseñas/posts (Xiaohongshu/Ctrip) por usuario
- Salida: arquetipo, confidence score, cultural triggers
"""
import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

ARCHETYPES = [
    'Old Money', 'New Rich', 'Cultural Academic', 'Digital Influencer', 'High-End Adventurer'
]

SYSTEM_PROMPT = (
    "Eres un analista de turismo de lujo. Clasifica el texto en uno de estos arquetipos: "
    + ', '.join(ARCHETYPES) + ". Devuelve JSON con: arquetipo, confidence_score (0-1), cultural_triggers (lista de palabras clave)."
)

def classify_luxury_persona(text):
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = SYSTEM_PROMPT + f"\nTexto: {text}"
    response = model.generate_content(prompt)
    try:
        result = json.loads(response.text)
    except Exception:
        result = {'arquetipo': None, 'confidence_score': 0, 'cultural_triggers': []}
    return result

if __name__ == '__main__':
    sample = "El hotel tenía un ambiente clásico y el personal hablaba varios idiomas. Compartí mi experiencia en Xiaohongshu."
    print(classify_luxury_persona(sample))
