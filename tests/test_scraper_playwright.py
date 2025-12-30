"""
Automated Playwright-based tests for Xiaohongshu Scraper
ENGLISH / ESPAÑOL / ESPERANTO

EN: Validates browser launch, hashtag extraction, URL and sentiment integrity, and performance.
ES: Valida el lanzamiento del navegador, extracción de hashtags, integridad de URLs y sentimiento, y el rendimiento.
EO: Validigas la lanĉon de la retumilo, ekstrakton de hashtagoj, integrecon de URL-oj kaj sentimon, kaj la rendimenton.
"""
import subprocess
import json
import time
import os
import pytest

SCRAPER_PATH = os.path.abspath("xiaohongshu_scraper.py")

@pytest.mark.timeout(40)
def test_scraper_output():
    """
    EN: Test that the scraper runs, outputs valid JSON, and meets data/performance requirements.
    ES: Prueba que el scraper se ejecuta, genera JSON válido y cumple requisitos de datos/rendimiento.
    EO: Testas ke la scraper funkcias, eligas validan JSON kaj plenumas datumajn/rendimentajn postulojn.
    """
    start = time.time()
    proc = subprocess.run(["python", SCRAPER_PATH], capture_output=True, text=True, timeout=40)
    assert proc.returncode == 0, f"Scraper failed: {proc.stderr}"
    # Find output file path in stdout
    out_path = None
    for line in proc.stdout.splitlines():
        if "Results written to" in line:
            out_path = line.split("Results written to")[-1].strip()
    assert out_path and os.path.exists(out_path), "Output JSON file not found."
    with open(out_path, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list) and len(data) >= 5, "Less than 5 hashtags extracted."
    for tag in data[:5]:
        assert isinstance(tag["post_count"], int) and tag["post_count"] > 0, "Invalid post_count."
        assert isinstance(tag["sample_posts"], list) and all(url.startswith("http") for url in tag["sample_posts"]), "Invalid sample_posts URLs."
        assert 0.0 <= tag["avg_sentiment"] <= 1.0, "avg_sentiment out of range."
    elapsed = time.time() - start
    assert elapsed < 30, f"Scraper took too long: {elapsed:.2f}s"
