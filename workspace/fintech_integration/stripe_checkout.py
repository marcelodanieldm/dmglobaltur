"""
Stripe Checkout & Billing Integration
- Multi-currency (EUR/USD/CNY)
- Supports Credit Card, Alipay, WeChat Pay
- Localized checkout
- Webhook for Supabase tier update
"""
import stripe
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# --- Stripe Checkout Session ---
@app.post("/api/v1/payments/checkout")
async def create_checkout_session(request: Request):
    data = await request.json()
    currency = data.get("currency", "usd")
    email = data.get("email")
    lang = data.get("lang", "en")
    price_id = data.get("price_id")
    session = stripe.checkout.Session.create(
        payment_method_types=["card", "alipay", "wechat_pay"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        customer_email=email,
        success_url=f"https://yourdomain.com/success?lang={lang}",
        cancel_url=f"https://yourdomain.com/cancel?lang={lang}",
        locale=lang,
    )
    return {"checkout_url": session.url}

# --- Stripe Customer Portal ---
@app.get("/api/v1/payments/portal")
async def customer_portal(email: str, lang: str = "en"):
    customers = stripe.Customer.list(email=email).data
    if not customers:
        raise HTTPException(404, "Customer not found")
    portal_session = stripe.billing_portal.Session.create(
        customer=customers[0].id,
        return_url=f"https://yourdomain.com/dashboard?lang={lang}"
    )
    return RedirectResponse(portal_session.url)

# --- Webhook Listener ---
@app.post("/api/v1/payments/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception:
        raise HTTPException(400, "Invalid webhook")
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["client_reference_id"]
        tier_id = session["display_items"][0]["price"]
        # Update Supabase tier_id (pseudo-code)
        # supabase.table("users").update({"tier_id": tier_id}).eq("id", user_id).execute()
    return {"status": "success"}

# --- Authorization Guard Middleware ---
from fastapi import Depends

def check_subscription(user_id: str):
    # Query Supabase for user's tier_id (pseudo-code)
    # tier = supabase.table("users").select("tier_id").eq("id", user_id).single().execute()
    # if tier not in ["premium", "enterprise"]:
    #     raise HTTPException(403, "Upgrade required")
    pass

@app.get("/api/v1/premium/forecasting")
async def premium_forecasting(user_id: str = Depends(check_subscription)):
    return {"result": "Premium forecasting data"}
