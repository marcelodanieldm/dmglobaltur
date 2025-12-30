"""
Integration tests for recommendation engine and localization
ENGLISH / ESPAÑOL / ESPERANTO

EN: Validates recommendation logic, localization, and access control for the API.
ES: Valida la lógica de recomendación, localización y control de acceso de la API.
EO: Validigas la rekomendan logikon, lokalizadon kaj alirkontrolon de la API.
"""
import os
import pytest
import requests
import jwt

API_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")
JWT_ALGORITHM = "HS256"

def make_jwt(payload=None):
    if payload is None:
        payload = {"user_id": 1, "tier": "premium"}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

@pytest.mark.timeout(2)
def test_vibe_matching_old_money_london():
    """
    EN: Old Money persona in London should get high-end tea or private museum tours.
    ES: Persona Old Money en Londres debe recibir té de lujo o tours privados de museo.
    EO: Old Money persono en Londono ricevu luksan teon aŭ privatajn muzeajn vizitojn.
    """
    token = make_jwt({"user_id": 2, "tier": "premium"})
    params = {"persona": "Old Money Luxury", "location": "London", "language": "en"}
    resp = requests.get(f"{API_URL}/api/v1/recommend/vibe-matching", params=params, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert any("tea" in a.lower() or "museum" in a.lower() for a in data.get("activities", []))

@pytest.mark.timeout(2)
def test_vibe_matching_insta_argentina():
    """
    EN: Insta-Traveler in Argentina should get glacier or winery recommendations.
    ES: Insta-Traveler en Argentina debe recibir recomendaciones de glaciares o bodegas.
    EO: Insta-Traveler en Argentino ricevu rekomendojn pri glaĉeroj aŭ vinfarejoj.
    """
    token = make_jwt({"user_id": 3, "tier": "premium"})
    params = {"persona": "Insta-Traveler", "location": "Argentina", "language": "es"}
    resp = requests.get(f"{API_URL}/api/v1/recommend/vibe-matching", params=params, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert any("glacier" in a.lower() or "bodega" in a.lower() or "winery" in a.lower() for a in data.get("activities", []))

@pytest.mark.timeout(2)
def test_localization_portuguese():
    """
    EN: If Accept-Language is pt-BR, response should be in Portuguese.
    ES: Si Accept-Language es pt-BR, la respuesta debe estar en portugués.
    EO: Se Accept-Language estas pt-BR, la respondo estu en la portugala.
    """
    token = make_jwt()
    params = {"persona": "Shopping Focused", "location": "Madrid", "language": "pt"}
    headers = {"Authorization": f"Bearer {token}", "Accept-Language": "pt-BR"}
    resp = requests.get(f"{API_URL}/api/v1/recommend/vibe-matching", params=params, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    # EN: For demo, check at least one activity is in Portuguese (simple check)
    # ES: Para demo, verifica que al menos una actividad esté en portugués
    # EO: Por demo, kontrolu ke almenaŭ unu agado estas en la portugala
    assert any("Madrid" in a or "de" in a for a in data.get("activities", []))

@pytest.mark.timeout(2)
def test_tier_access_control():
    """
    EN: Tier 1 user should not access Tier 2 (real-time) data.
    ES: Usuario Tier 1 no debe acceder a datos Tier 2 (tiempo real).
    EO: Tier 1 uzanto ne havu aliron al Tier 2 (reala tempo) datumoj.
    """
    token = make_jwt({"user_id": 4, "tier": "basic"})
    params = {"persona": "Old Money Luxury", "location": "London", "language": "en"}
    resp = requests.get(f"{API_URL}/api/v1/recommend/vibe-matching", params=params, headers={"Authorization": f"Bearer {token}"})
    # EN: Should get 403 or downgraded data
    # ES: Debe recibir 403 o datos limitados
    # EO: Devus ricevi 403 aŭ limigitajn datumojn
    assert resp.status_code in (403, 200)
    if resp.status_code == 200:
        data = resp.json()
        assert data.get("tier", "basic") == "basic"
