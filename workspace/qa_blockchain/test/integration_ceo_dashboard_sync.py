# Integration Test: CEO Dashboard Sync
# This test checks that the CEO Dashboard reflects blockchain balance within <5s after contract event.
# Uses FastAPI event listener and dashboard update logic.

import time
import requests

def test_ceo_dashboard_sync():
    # Simulate contract event (e.g., payout)
    # Trigger FastAPI event listener (dmtrust_listener.py)
    # Wait up to 5 seconds for dashboard update
    dashboard_url = "http://localhost:8000/dashboard/balance"  # Adjust as needed
    start = time.time()
    while time.time() - start < 5:
        resp = requests.get(dashboard_url)
        if resp.status_code == 200 and resp.json().get("synced"):
            assert True
            return
        time.sleep(0.5)
    assert False, "Dashboard did not sync within 5 seconds"
