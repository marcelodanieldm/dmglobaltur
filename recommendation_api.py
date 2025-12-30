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

# Mock inventory DB
MOCK_INVENTORY = {
    "Madrid": [
        {"item": "Hermès Birkin", "stock_cn": 1, "stock_dest": 5},
        {"item": "Rolex Daytona", "stock_cn": 0, "stock_dest": 3},
        {"item": "Louis Vuitton Capucines", "stock_cn": 2, "stock_dest": 7}
    ],
    "Paris": [
        {"item": "Chanel Classic Flap", "stock_cn": 0, "stock_dest": 4},
        {"item": "Dior Book Tote", "stock_cn": 1, "stock_dest": 6}
    ]
}

# Mock activities DB
MOCK_ACTIVITIES = {
    "Madrid": {
        "Old Money Luxury": ["Private Prado Museum Tour", "Gourmet Tapas Crawl", "Luxury Shopping at Salamanca"],
        "Adventure Seeker": ["Hot Air Balloon Ride", "Segovia Hiking", "Kayak in Manzanares"],
        "Shopping Focused": ["Las Rozas Village Outlet", "El Corte Inglés VIP", "Designer Pop-Up Events"],
        "Cultural Immersion": ["Flamenco Masterclass", "Royal Palace Tour", "Local Artisanal Markets"],
        "Insta-Traveler": ["Gran Via Rooftop Photoshoot", "Retiro Park Picnic", "Street Art Tour"]
    },
    "Paris": {
        "Old Money Luxury": ["Private Louvre Tour", "Michelin Star Dining", "Chauffeured Seine Cruise"],
        "Adventure Seeker": ["Versailles Bike Tour", "Montmartre Climbing", "Seine Kayaking"],
        "Shopping Focused": ["Galeries Lafayette VIP", "Le Marais Boutiques", "Luxury Outlet Day"],
        "Cultural Immersion": ["Wine & Cheese Tasting", "Opera Garnier Tour", "Montparnasse Artists Walk"],
        "Insta-Traveler": ["Eiffel Tower Sunrise", "Montmartre Murals", "Champs-Élysées Selfie Spots"]
    }
}

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
    EN: Return items with low stock in China but high stock in the destination.
    ES: Devuelve artículos con poco stock en China pero alto en el destino.
    EO: Redonu varojn kun malmulta stoko en Ĉinio sed multe en la celo.
    """
    cache_key = f"scarcity:{dest}"
    cached = await get_cached(cache_key)
    if cached:
        return cached
    items = [item for item in MOCK_INVENTORY.get(dest, []) if item["stock_cn"] < 2 and item["stock_dest"] > 2]
    result = {"destination": dest, "scarce_items": items}
    await set_cached(cache_key, result)
    return result

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# EN: To run: uvicorn recommendation_api:app --reload
# ES: Para ejecutar: uvicorn recommendation_api:app --reload
# EO: Por lanĉi: uvicorn recommendation_api:app --reload
