"""
Automated tests for recommendation_api.py
ENGLISH / ESPAÑOL / ESPERANTO

EN: Validates cultural logic, language response, and API performance for recommendation endpoints.
ES: Valida la lógica cultural, la respuesta en idioma y el rendimiento de la API de recomendaciones.
EO: Validigas la kulturan logikon, lingvan respondon kaj API-rendimenton por rekomendaj finoj.
"""
import os
import pytest
import requests
import jwt
import time

API_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")
JWT_ALGORITHM = "HS256"

# Helper to create JWT
def make_jwt(payload=None):
    if payload is None:
        payload = {"user_id": 1, "tier": "premium"}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

@pytest.mark.timeout(2)
def test_vibe_matching_cultural():
    """
    EN: Test that vibe-matching returns culturally relevant activities for Madrid and persona.
    ES: Prueba que vibe-matching devuelve actividades culturalmente relevantes para Madrid y persona.
    EO: Testas ke vibe-matching redonas kulture gravajn agadojn por Madrido kaj persono.
    """
    token = make_jwt()
    params = {"persona": "Cultural Immersion", "location": "Madrid", "language": "es"}
    t0 = time.time()
    resp = requests.get(f"{API_URL}/api/v1/recommend/vibe-matching", params=params, headers={"Authorization": f"Bearer {token}"})
    elapsed = time.time() - t0
    assert resp.status_code == 200
    data = resp.json()
    # EN: Check for at least one culturally relevant activity
    # ES: Verifica al menos una actividad culturalmente relevante
    # EO: Kontrolu almenaŭ unu kulture gravan agadon
    assert any("Flamenco" in a or "Palace" in a or "Artisanal" in a for a in data.get("activities", []))
    assert elapsed < 0.5

@pytest.mark.timeout(2)
def test_scarcity_language():
    """
    EN: Test that scarcity endpoint returns items and responds in English by default.
    ES: Prueba que el endpoint de escasez devuelve artículos y responde en inglés por defecto.
    EO: Testas ke la fino de malabundo redonas varojn kaj respondas angle defaŭlte.
    """
    token = make_jwt()
    params = {"dest": "Madrid"}
    resp = requests.get(f"{API_URL}/api/v1/recommend/scarcity", params=params, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    # EN: Check for at least one item with high stock_dest
    # ES: Verifica al menos un artículo con alto stock_dest
    # EO: Kontrolu almenaŭ unu varon kun alta stock_dest
    assert any(item["stock_dest"] > 2 for item in data.get("scarce_items", []))
    # EN: Check response keys are in English
    # ES: Verifica que las claves de respuesta estén en inglés
    # EO: Kontrolu ke la respondaj ŝlosiloj estas angle
    assert "destination" in data and "scarce_items" in data

@pytest.mark.timeout(2)
def test_vibe_matching_language_toggle():
    """
    EN: Test that the API can respond in Mandarin if requested (simulate by language param).
    ES: Prueba que la API puede responder en mandarín si se solicita (simulado por parámetro language).
    EO: Testas ke la API povas respondi en la mandarena se oni petas (simulita per language-parametro).
    """
    token = make_jwt()
    params = {"persona": "Shopping Focused", "location": "Madrid", "language": "zh"}
    resp = requests.get(f"{API_URL}/api/v1/recommend/vibe-matching", params=params, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    # EN: For demo, just check the response is present
    # ES: Para demo, solo verifica que hay respuesta
    # EO: Por demo, nur kontrolu ke estas respondo
    assert "activities" in data
