"""
FastAPI backend for real-time funnel dashboard data
- Serves Opportunity Reports from FreemiumScorer
"""
from fastapi import FastAPI
from freemium_scoring import FreemiumScorer

app = FastAPI()
scorer = FreemiumScorer()

# Simulate user events (replace with real DB integration)
for user_id in ["user123", "user456"]:
    scorer.log_event(user_id, "signup", {})
    scorer.log_event(user_id, "hashtag_found", {"hashtag": "#travel"})
    for _ in range(3):
        scorer.log_event(user_id, "city_query", {"city": "Paris"})

@app.get("/api/v1/funnel/reports")
def get_reports():
    reports = []
    for user_id in scorer.user_events.keys():
        report = scorer.generate_opportunity_report(user_id)
        reports.append({
            "user_id": report["user_id"],
            "time_to_value": report["time_to_value"],
            "high_intent": report["high_intent"],
            "recommendation": report["recommendation"]
        })
    return {"reports": reports}
