"""
Freemium Scoring Model for Lead-to-Cash Funnel
- Tracks Time-to-Value
- Flags High Intent users
- Generates Opportunity Report (Gemini 1.5 Flash API placeholder)
"""
import time
from collections import defaultdict

class FreemiumScorer:
    def __init__(self):
        self.user_events = defaultdict(list)  # {user_id: [(timestamp, event_type, details)]}
        self.high_intent_flags = set()

    def log_event(self, user_id, event_type, details):
        self.user_events[user_id].append((time.time(), event_type, details))

    def time_to_value(self, user_id):
        events = self.user_events[user_id]
        signup_time = next((t for t, e, d in events if e == "signup"), None)
        hashtag_time = next((t for t, e, d in events if e == "hashtag_found"), None)
        if signup_time and hashtag_time:
            return hashtag_time - signup_time
        return None

    def check_high_intent(self, user_id):
        now = time.time()
        city_queries = [t for t, e, d in self.user_events[user_id] if e == "city_query" and now - t < 86400]
        if len(city_queries) >= 3:
            self.high_intent_flags.add(user_id)
            return True
        return False

    def generate_opportunity_report(self, user_id):
        # Placeholder for Gemini 1.5 Flash API call
        events = self.user_events[user_id]
        ttv = self.time_to_value(user_id)
        high_intent = user_id in self.high_intent_flags
        report = {
            "user_id": user_id,
            "time_to_value": ttv,
            "high_intent": high_intent,
            "event_summary": events,
            "recommendation": "Send personalized upgrade offer."
        }
        # In real use, call Gemini API here
        return report

# Example usage
if __name__ == "__main__":
    scorer = FreemiumScorer()
    scorer.log_event("user123", "signup", {})
    time.sleep(1)
    scorer.log_event("user123", "hashtag_found", {"hashtag": "#travel"})
    for _ in range(3):
        scorer.log_event("user123", "city_query", {"city": "Paris"})
    print("Time-to-Value:", scorer.time_to_value("user123"))
    print("High Intent:", scorer.check_high_intent("user123"))
    print("Opportunity Report:", scorer.generate_opportunity_report("user123"))
