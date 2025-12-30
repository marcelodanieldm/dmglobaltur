"""
Automated Pytest-based API tests for FastAPI backend
ENGLISH / ESPAÑOL / ESPERANTO

EN: Validates ingestion, retrieval, rate-limiting, and performance of the API.
ES: Valida la ingesta, consulta, limitación de tasa y rendimiento de la API.
EO: Validigas la enigon, ricevon, limigon de petfrekvenco kaj rendimenton de la API.
"""
import os
import pytest
import requests
import time

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "changeme")

@pytest.mark.timeout(2)
def test_health():
    resp = requests.get(f"{BASE_URL}/health")
    assert resp.status_code == 200

@pytest.mark.timeout(2)
def test_ingest_valid():
    payload = [
        {"hashtag": "#Test", "post_count": 123, "sample_posts": ["http://test.com"], "avg_sentiment": 0.8}
    ]
    t0 = time.time()
    resp = requests.post(f"{BASE_URL}/api/v1/ingest/xiaohongshu", json=payload)
    elapsed = time.time() - t0
    assert resp.status_code == 201
    assert resp.json().get("status") == "success"
    assert elapsed < 0.5

@pytest.mark.timeout(2)
def test_ingest_invalid():
    resp = requests.post(f"{BASE_URL}/api/v1/ingest/xiaohongshu", json={"bad": "data"})
    assert resp.status_code in (400, 422)

@pytest.mark.timeout(2)
def test_get_trends():
    t0 = time.time()
    resp = requests.get(f"{BASE_URL}/api/v1/trends/xiaohongshu", headers={"X-API-Key": API_KEY})
    elapsed = time.time() - t0
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) <= 10
    for trend in data:
        assert "hashtag" in trend and "post_count" in trend and "sample_posts" in trend and "avg_sentiment" in trend
    assert elapsed < 0.2

@pytest.mark.timeout(5)
def test_rate_limit():
    # Exceed rate limit
    for _ in range(105):
        resp = requests.get(f"{BASE_URL}/api/v1/trends/xiaohongshu", headers={"X-API-Key": API_KEY})
    assert resp.status_code == 429
