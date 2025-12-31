"""
Abandoned Cart Recovery Flow
- Detects abandoned checkouts (no success in 30 min)
- Sends reminder email (localized for China)
- Generates Stripe coupon after 24h if unpaid
- Reports recovered revenue to CEO Dashboard
"""
import time
import threading
import stripe
import smtplib
from email.mime.text import MIMEText

stripe.api_key = 'sk_test_xxx'  # Replace with env var in production

# In-memory store for demo
pending_checkouts = {}
recovered_revenue = 0

# --- Event: User reaches checkout ---
def track_checkout(user_id, email, ip, price_id, session_id):
    pending_checkouts[session_id] = {
        'user_id': user_id,
        'email': email,
        'ip': ip,
        'price_id': price_id,
        'start_time': time.time(),
        'reminder_sent': False,
        'coupon_sent': False,
        'completed': False
    }
    threading.Thread(target=monitor_checkout, args=(session_id,)).start()

# --- Monitor for abandonment ---
def monitor_checkout(session_id):
    checkout = pending_checkouts[session_id]
    # Wait 30 min for success event
    for _ in range(60):
        if checkout['completed']:
            return
        time.sleep(30)
    if not checkout['reminder_sent']:
        send_reminder_email(checkout)
        checkout['reminder_sent'] = True
    # Wait up to 24h for payment
    for _ in range(46):
        if checkout['completed']:
            return
        time.sleep(1800)
    if not checkout['coupon_sent']:
        send_coupon(checkout)
        checkout['coupon_sent'] = True

# --- Stripe webhook: mark as completed ---
def mark_checkout_completed(session_id):
    if session_id in pending_checkouts:
        pending_checkouts[session_id]['completed'] = True
        global recovered_revenue
        recovered_revenue += 1  # Replace with real amount

# --- Action 1: Send reminder email ---
def send_reminder_email(checkout):
    is_china = checkout['ip'].startswith('CN')  # Replace with real IP check
    subject = "Su acceso a los datos de lujo de Madrid está esperando (Alipay disponible)" if is_china else "Your luxury data access is waiting"
    body = "Hi,\n\nYou left something valuable in your cart! Complete your purchase to access premium travel data."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'sales@dmglobaltur.com'
    msg['To'] = checkout['email']
    print(f"Sending reminder to {checkout['email']} (subject: {subject})")
    # Uncomment for real SMTP
    # smtp = smtplib.SMTP('smtp.example.com')
    # smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
    # smtp.quit()

# --- Action 2: Generate Stripe coupon ---
def send_coupon(checkout):
    coupon = stripe.Coupon.create(
        percent_off=10,
        duration='once',
        max_redemptions=1
    )
    body = f"Hi,\n\nHere's a 10% discount for your first month: {coupon.id}"
    msg = MIMEText(body)
    msg['Subject'] = "Special offer: 10% off your first month!"
    msg['From'] = 'sales@dmglobaltur.com'
    msg['To'] = checkout['email']
    print(f"Sending coupon to {checkout['email']} (coupon: {coupon.id})")
    # Uncomment for real SMTP
    # smtp = smtplib.SMTP('smtp.example.com')
    # smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
    # smtp.quit()

# --- Tracking for CEO Dashboard ---
def get_recovered_revenue():
    return recovered_revenue
