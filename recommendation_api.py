"""
recommendation_api.py
ENGLISH / ESPAÑOL / ESPERANTO

EN: FastAPI endpoints for Vibe-Matching and Scarcity/Opportunity recommendations with JWT auth and Redis caching.
ES: Endpoints FastAPI para recomendaciones de Vibe-Matching y Escasez/Oportunidad con autenticación JWT y caché Redis.
EO: FastAPI-finoj por Vibe-Matching kaj Malabundo/Ŝanco-rekomendoj kun JWT-aŭtentikigo kaj Redis-kaŝmemoro.
"""
import os
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any
import jwt
import redis.asyncio as redis
import asyncio
import random
import base64
from cryptography.fernet import Fernet
import googletrans

# Redis config
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# JWT config
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")
JWT_ALGORITHM = "HS256"

# FastAPI app
app = FastAPI(title="DM Global Tur Recommendation API",
              description="Vibe-Matching and Scarcity endpoints for luxury travel SaaS.",
              version="1.0.0")

# Security
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            try:
                payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                request.state.user = payload
                return credentials.credentials
            except jwt.PyJWTError:
                raise HTTPException(status_code=403, detail="Invalid JWT token")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

def get_user(request: Request):
    return request.state.user

# Models
class UserProfile(BaseModel):
    persona: str
    language: str = "zh"
    location: str
    tier: str = "basic"

class ScarcityRequest(BaseModel):
    destination: str
    category: str = "luxury retail"

# --- Business Rule: Margins for Scarcity ---
# Add margin to inventory
MOCK_INVENTORY = {
    "Madrid": [
        {"item": "Hermès Birkin", "stock_cn": 1, "stock_dest": 5, "margin": 0.45},
        {"item": "Rolex Daytona", "stock_cn": 0, "stock_dest": 3, "margin": 0.38},
        {"item": "Louis Vuitton Capucines", "stock_cn": 2, "stock_dest": 7, "margin": 0.33}
    ],
    "Paris": [
        {"item": "Chanel Classic Flap", "stock_cn": 0, "stock_dest": 4, "margin": 0.41},
        {"item": "Dior Book Tote", "stock_cn": 1, "stock_dest": 6, "margin": 0.29}
    ]
}

# --- Business Rule: End-to-End Encryption for Inventory ---
FERNET_KEY = os.getenv("INVENTORY_FERNET_KEY") or Fernet.generate_key().decode()
fernet = Fernet(FERNET_KEY.encode())

def encrypt_inventory(data):
    """
    EN: Encrypt inventory data for secure sharing.
    ES: Cifra datos de inventario para compartir seguro.
    EO: Ĉifru inventardatumojn por sekura kunhavigo.
    """
    import json
    return fernet.encrypt(json.dumps(data).encode()).decode()

def decrypt_inventory(token):
    import json
    return json.loads(fernet.decrypt(token.encode()).decode())

# --- Business Rule: Multilingual Dynamic Prediction ---
translator = googletrans.Translator()
LANG_MAP = {
    "Brazil": "pt",
    "France": "fr",
    "China": "zh-cn",
    # Add more as needed
}
MANDARIN = "zh-cn"

def translate_with_original(text, dest_lang):
    """
    EN: Translate text to dest_lang, always include Mandarin original.
    ES: Traduce texto a dest_lang, siempre incluye original en mandarín.
    EO: Traduku tekston al dest_lang, ĉiam inkluzivu mandarenan originalon.
    """
    mandarin = translator.translate(text, dest=MANDARIN).text
    translated = translator.translate(text, dest=dest_lang).text
    return {"translated": translated, "original_mandarin": mandarin}

# Geo-fencing logic
def prioritize_region(location: str, destination: str, data: dict) -> dict:
    # EN: If user is in South America, prioritize South American destinations
    # ES: Si el usuario está en Sudamérica, prioriza destinos sudamericanos
    # EO: Se uzanto estas en Sudameriko, prioritatigu sudamerikajn celojn
    south_america = ["Brazil", "Argentina", "Chile", "Peru", "Colombia"]
    if location in south_america and destination not in south_america:
        # For demo, just return as is, but could filter or boost South American data
        pass
    return data

# Redis cache helpers
async def get_cached(key: str):
    val = await redis_client.get(key)
    if val:
        import json
        return json.loads(val)
    return None

async def set_cached(key: str, value: dict, expire: int = 3600):
    import json
    await redis_client.set(key, json.dumps(value), ex=expire)

# Vibe-Matching endpoint
@app.get("/api/v1/recommend/vibe-matching", dependencies=[Depends(JWTBearer())])
async def vibe_matching(profile: UserProfile = Depends(), user=Depends(get_user)):
    """
    EN: Recommend 3 activities in the destination based on persona and sentiment.
    ES: Recomienda 3 actividades en el destino según la persona y el sentimiento.
    EO: Rekomendu 3 agadojn en la celo laŭ persono kaj sentimo.
    """
    cache_key = f"vibe:{profile.persona}:{profile.location}"
    cached = await get_cached(cache_key)
    if cached:
        return cached
    # Mock: Use persona and location to select activities
    activities = MOCK_ACTIVITIES.get(profile.location, {}).get(profile.persona, [])
    if not activities:
        activities = random.sample(sum([v for v in MOCK_ACTIVITIES.get(profile.location, {}).values()], []), 3) if MOCK_ACTIVITIES.get(profile.location) else []
    result = {"destination": profile.location, "persona": profile.persona, "activities": activities[:3]}
    await set_cached(cache_key, result)
    return result

# Scarcity endpoint
@app.get("/api/v1/recommend/scarcity", dependencies=[Depends(JWTBearer())])
async def scarcity(dest: str, user=Depends(get_user)):
    """
    EN: Return items with low stock in China but high stock in the destination, prioritized by profit margin. Data is end-to-end encrypted.
    ES: Devuelve artículos con poco stock en China pero alto en el destino, priorizados por margen de ganancia. Datos cifrados de extremo a extremo.
    EO: Redonu varojn kun malmulta stoko en Ĉinio sed multe en la celo, prioritatigitaj laŭ profita marĝeno. Datumoj estas ĉifritaj de ekstremo al ekstremo.
    """
    cache_key = f"scarcity:{dest}"
    cached = await get_cached(cache_key)
    if cached:
        return cached
    items = [item for item in MOCK_INVENTORY.get(dest, []) if item["stock_cn"] < 2 and item["stock_dest"] > 2]
    # Prioritize by margin
    items = sorted(items, key=lambda x: x["margin"], reverse=True)
    # Encrypt inventory
    encrypted = encrypt_inventory(items)
    result = {"destination": dest, "scarce_items_encrypted": encrypted}
    await set_cached(cache_key, result)
    return result

@app.get("/api/v1/recommend/scarcity/decrypt", dependencies=[Depends(JWTBearer())])
async def scarcity_decrypt(token: str, user=Depends(get_user)):
    """
    EN: Decrypt inventory data (for trusted partners).
    ES: Descifra datos de inventario (para aliados de confianza).
    EO: Malĉifru inventardatumojn (por fidindaj partneroj).
    """
    return {"decrypted": decrypt_inventory(token)}

@app.get("/api/v1/recommend/predict-multilingual", dependencies=[Depends(JWTBearer())])
async def predict_multilingual(destination: str, text: str, dmc_lang: str = None):
    """
    EN: Predict in DMC language, always include Mandarin original.
    ES: Predice en el idioma del DMC, siempre incluye original en mandarín.
    EO: Prognozu en la DMC-lingvo, ĉiam inkluzivu mandarenan originalon.
    """
    lang = dmc_lang or LANG_MAP.get(destination, "en")
    return translate_with_original(text, lang)

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# EN: To run: uvicorn recommendation_api:app --reload
# ES: Para ejecutar: uvicorn recommendation_api:app --reload
# EO: Por lanĉi: uvicorn recommendation_api:app --reload
