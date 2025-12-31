"""
FastAPI backend for Financial Command Center
- Serves real-time MRR, cost, CAC, LTV, and burn rate metrics
- Connects to Stripe, Supabase, Gemini (placeholders)
"""
from fastapi import FastAPI
import random
from cart_recovery.abandoned_cart_recovery import get_recovered_revenue

app = FastAPI()

# Placeholder: Replace with real Stripe/Supabase/Gemini API calls
@app.get("/api/v1/financial/mrr")
def get_mrr():
    return {"labels": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], "data": [12000, 13500, 14200, 15000, 15800, 16500]}

@app.get("/api/v1/financial/cost_revenue")
def get_cost_revenue():
    return {
        "labels": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "gemini_cost": [800, 950, 1100, 1200, 1300, 1400],
        "user_revenue": [12000, 13500, 14200, 15000, 15800, 16500]
    }

@app.get("/api/v1/financial/metrics")
def get_metrics():
    return {
        "net_burn_rate": -2500,
        "cac": 120,
        "ltv": 2800
    }

@app.post("/api/v1/financial/manual_override")
def manual_override(user_id: str):
    # Simulate granting premium access
    return {"status": "Premium access granted to user " + user_id}

@app.get("/api/v1/financial/recovered_revenue")
def get_recovered_revenue_api():
    return {"recovered_revenue": get_recovered_revenue()}
