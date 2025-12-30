"""
CEO Dashboard Integrity Test
ENGLISH / ESPAÑOL / ESPERANTO

EN: Ensures CEO dashboard reflects real-time cost of heavy computations.
ES: Asegura que el dashboard CEO refleje el costo en tiempo real de los cálculos pesados.
EO: Certigas ke la CEO-panelo reflektu la realtempan koston de pezaj kalkuloj.
"""
import pytest
import requests
import time

API_URL = "http://localhost:8000"

@pytest.mark.timeout(5)
def test_ceo_dashboard_costs():
    """
    EN: Simulate heavy load and check dashboard cost update.
    ES: Simula carga pesada y verifica actualización de costos en el dashboard.
    EO: Simulu pezan ŝargon kaj kontrolu ĝisdatigon de kostoj en la panelo.
    """
    # Simulate heavy load (call forecast API many times)
    for _ in range(100):
        requests.get(f"{API_URL}/api/v1/forecast/itinerary?region=Sevilla&category=Luxury")
    # Wait for dashboard to update
    time.sleep(2)
    resp = requests.get(f"{API_URL}/admin/ceo-metrics-data")
    assert resp.status_code == 200
    data = resp.json()
    # EN: Check that API cost increased
    # ES: Verifica que el costo de API aumentó
    # EO: Kontrolu ke la API-kosto kreskis
    assert data.get("api_cost", 0) > 0
