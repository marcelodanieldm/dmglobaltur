"""
intelligence_engine.py
ENGLISH / ESPAÑOL / ESPERANTO

EN: Multi-language sentiment, intent, and persona classification engine using Gemini 1.5 Flash API.
ES: Motor de clasificación de sentimiento, intención y persona multilingüe usando Gemini 1.5 Flash API.
EO: Plurlingva sentima, intenca kaj persona klasifika motoro uzante Gemini 1.5 Flash API.
"""
import os
import aiohttp
import asyncio
from typing import List, Dict, Any

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Personas
PERSONAS = [
    "Old Money Luxury",
    "Adventure Seeker",
    "Shopping Focused",
    "Cultural Immersion",
    "Insta-Traveler"
]

# Intents
INTENTS = ["Purchase Intent", "Aspiration", "Complaint"]

async def call_gemini(prompt: str, session: aiohttp.ClientSession) -> str:
    """
    EN: Call Gemini 1.5 Flash API with a prompt and return the response text.
    ES: Llama a Gemini 1.5 Flash API con un prompt y devuelve el texto de respuesta.
    EO: Voku Gemini 1.5 Flash API per prompto kaj redonu la respondan tekston.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    params = {"key": GEMINI_API_KEY}
    async with session.post(GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=15) as resp:
        data = await resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

async def enrich_caption(caption: str, destination: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
    """
    EN: Enrich a caption with translation, sentiment, intent, persona, and expectation-gap.
    ES: Enriquece un caption con traducción, sentimiento, intención, persona y expectation-gap.
    EO: Riĉigu caption per traduko, sentimo, intenco, persono kaj expectation-gap.
    """
    # 1. Translate
    prompt_translate = (
        f"Translate the following text to English, Spanish, and Portuguese, keeping the original tone.\nText: {caption}\n"
        "Return as JSON: {\"en\":..., \"es\":..., \"pt\":...}"
    )
    translation = await call_gemini(prompt_translate, session)
    # 2. Sentiment & Intent & Persona
    prompt_classify = (
        f"Analyze the following travel review.\nText: {caption}\n"
        "Return JSON: {\"sentiment\": -1.0~1.0, \"intent\": one of ['Purchase Intent','Aspiration','Complaint'], "
        "\"persona\": one of ['Old Money Luxury','Adventure Seeker','Shopping Focused','Cultural Immersion','Insta-Traveler']}"
    )
    classification = await call_gemini(prompt_classify, session)
    # 3. Expectation-Gap
    prompt_gap = (
        f"Destination: {destination}\nUser review: {caption}\n"
        "Compare the destination's typical promise (luxury, culture, shopping, etc.) with the user's sentiment. "
        "Return a single float between -1.0 (big disappointment) and 1.0 (exceeded expectations) as 'expectation_gap'."
    )
    gap = await call_gemini(prompt_gap, session)
    # Parse responses (simple eval, in production use json.loads with validation)
    try:
        translation_json = eval(translation)
    except Exception:
        translation_json = {"en": caption, "es": caption, "pt": caption}
    try:
        classification_json = eval(classification)
    except Exception:
        classification_json = {"sentiment": 0.0, "intent": "Aspiration", "persona": "Insta-Traveler"}
    try:
        gap_value = float(gap)
    except Exception:
        gap_value = 0.0
    return {
        "translations": translation_json,
        "sentiment": classification_json.get("sentiment", 0.0),
        "intent": classification_json.get("intent", "Aspiration"),
        "persona": classification_json.get("persona", "Insta-Traveler"),
        "expectation_gap": gap_value
    }

async def enrich_captions_batch(captions: List[str], destination: str) -> List[Dict[str, Any]]:
    """
    EN: Enrich a batch of captions.
    ES: Enriquece un lote de captions.
    EO: Riĉigu aron da caption-oj.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [enrich_caption(c, destination, session) for c in captions]
        return await asyncio.gather(*tasks)

# Example usage / Ejemplo de uso / Ekzemplo de uzo
if __name__ == "__main__":
    captions = [
        "酒店很漂亮，但服务一般，价格偏高。",
        "Increíble experiencia de compras en París, ¡volvería!",
        "The cultural sites were breathtaking, but too crowded."
    ]
    destination = "Paris"
    results = asyncio.run(enrich_captions_batch(captions, destination))
    for r in results:
        print(r)
