"""
Backtesting and QA for Forecasting Engine
ENGLISH / ESPAÑOL / ESPERANTO

EN: Compares 15-day forecasts to actuals and computes MAPE for accuracy.
ES: Compara los pronósticos de 15 días con los datos reales y calcula MAPE para precisión.
EO: Komparas 15-tagan prognozon kun realaj datumoj kaj kalkulas MAPE por precizeco.
"""
import pandas as pd
import numpy as np
import requests
import os

API_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8)))

def test_forecast_backtesting():
    """
    EN: Backtest the forecast API for accuracy.
    ES: Backtesting de la API de pronóstico para precisión.
    EO: Malantaŭa testado de la prognoza API por precizeco.
    """
    # Simulate historical actuals
    actuals = np.random.randint(50, 200, 15)
    # Get forecast from API
    resp = requests.get(f"{API_URL}/api/v1/forecast/itinerary", params={"region": "Sevilla", "category": "Luxury"})
    assert resp.status_code == 200
    forecast = resp.json().get("forecast", [])
    assert len(forecast) == 15
    score = mape(actuals, forecast)
    print(f"MAPE: {score:.2%}")
    assert score < 0.35  # EN: Acceptable error <35%
