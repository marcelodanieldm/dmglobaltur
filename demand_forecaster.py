"""
demand_forecaster.py
ENGLISH / ESPAÑOL / ESPERANTO

EN: Influencer-Led Forecasting engine for predicting tourist demand surges using time-series and graph theory.
ES: Motor de predicción liderado por influencers para anticipar picos de demanda turística usando series temporales y teoría de grafos.
EO: Prognozilo gvidata de influenculoj por antaŭvidi turisman postulon per tempaj serioj kaj grafa teorio.
"""
import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from prophet import Prophet
import aiohttp
import asyncio

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def call_gemini_summary(text: str, session: aiohttp.ClientSession) -> str:
    """
    EN: Summarize why a destination is trending using Gemini 1.5 Flash.
    ES: Resume por qué un destino es tendencia usando Gemini 1.5 Flash.
    EO: Resumu kial celo estas tendenco per Gemini 1.5 Flash.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"Summarize in 1 sentence why this destination is trending: {text}"}]}]
    }
    params = {"key": GEMINI_API_KEY}
    async with session.post(GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=15) as resp:
        data = await resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

def viral_velocity_score(df: pd.DataFrame, influencer_col: str = "follower_count") -> float:
    """
    EN: Calculate how fast a destination is spreading (Viral Velocity Score).
    ES: Calcula la velocidad de viralización de un destino.
    EO: Kalkulu la virusan rapidecon de celo.
    """
    # Simple: growth rate of posts weighted by influencer reach
    df = df.sort_values("date")
    recent = df.tail(7)
    prev = df.tail(14).head(7)
    growth = (recent["volume"].sum() - prev["volume"].sum()) / (prev["volume"].sum() + 1)
    reach = recent[influencer_col].sum() / (prev[influencer_col].sum() + 1)
    return float(np.clip(growth * reach, 0, 1))

def forecast_demand(df: pd.DataFrame, arrivals: pd.DataFrame, periods: int = 15) -> Dict[str, Any]:
    """
    EN: Forecast demand using Prophet, correlating social engagement and arrivals.
    ES: Predice demanda usando Prophet, correlacionando engagement social y llegadas.
    EO: Prognozu postulon per Prophet, korelaciigante socian engaĝiĝon kaj alvenojn.
    """
    # Merge hashtag volume and arrivals
    df = df.copy()
    arrivals = arrivals.copy()
    df["ds"] = pd.to_datetime(df["date"])
    df["y"] = df["volume"] + df["follower_count"] * 0.0001
    m = Prophet()
    m.fit(df[["ds", "y"]])
    future = m.make_future_dataframe(periods=periods)
    forecast = m.predict(future)
    surge = float((forecast["yhat"].tail(periods).max() - df["y"].mean()) / (df["y"].mean() + 1))
    conf = float(forecast["yhat_upper"].tail(periods).mean() - forecast["yhat_lower"].tail(periods).mean()) / (forecast["yhat"].tail(periods).mean() + 1)
    return {
        "forecast": forecast,
        "predicted_surge": np.clip(surge, 0, 1),
        "confidence_interval": np.clip(conf, 0, 1)
    }

async def influencer_led_forecast(destination: str, hashtag_df: pd.DataFrame, arrivals_df: pd.DataFrame) -> Dict[str, Any]:
    """
    EN: Main function to run influencer-led forecasting and output enriched JSON.
    ES: Función principal para ejecutar la predicción liderada por influencers y devolver JSON enriquecido.
    EO: Ĉefa funkcio por ruli influenculan prognozon kaj redoni riĉigitan JSON.
    """
    # 1. Viral velocity
    vvs = viral_velocity_score(hashtag_df)
    # 2. Forecast
    result = forecast_demand(hashtag_df, arrivals_df)
    # 3. Recommended action (simple rule-based)
    if result["predicted_surge"] > 0.2:
        action = "Increase luxury SUV fleet"
    else:
        action = "Monitor demand"
    # 4. Gemini summary
    async with aiohttp.ClientSession() as session:
        why = await call_gemini_summary(" ".join(hashtag_df["caption"].tail(10)), session)
    return {
        "destination": destination,
        "predicted_surge": round(result["predicted_surge"], 2),
        "confidence_interval": round(result["confidence_interval"], 2),
        "viral_velocity_score": round(vvs, 2),
        "recommended_action": action,
        "why_trending": why
    }

# Example usage / Ejemplo de uso / Ekzemplo de uzo
if __name__ == "__main__":
    # Simulated data
    hashtag_df = pd.DataFrame({
        "date": pd.date_range("2025-12-01", periods=21),
        "volume": np.random.randint(10, 100, 21),
        "follower_count": np.random.randint(1000, 100000, 21),
        "caption": ["Influencer post about Sevilla"]*21
    })
    arrivals_df = pd.DataFrame({
        "date": pd.date_range("2025-12-01", periods=21),
        "arrivals": np.random.randint(50, 200, 21)
    })
    result = asyncio.run(influencer_led_forecast("Sevilla", hashtag_df, arrivals_df))
    print(result)
