"""
Edge Node Validation for Forecast API
ENGLISH / ESPAÑOL / ESPERANTO

EN: Verifies that requests from Tokyo hit the Asia node, not US-East.
ES: Verifica que las peticiones desde Tokio lleguen al nodo Asia, no US-East.
EO: Kontrolas ke petoj el Tokio trafas la Azian nodon, ne US-East.
"""
import pytest
from playwright.sync_api import sync_playwright

EDGE_URL = "https://api.dmglobaltur.com/api/v1/forecast/itinerary"

@pytest.mark.timeout(10)
def test_edge_routing_tokyo():
    """
    EN: Simulate request from Tokyo and check response header for Asia node.
    ES: Simula petición desde Tokio y verifica header de respuesta para nodo Asia.
    EO: Simulu peton el Tokio kaj kontrolu respondan header por Azia nodo.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(proxy={"server": "http://tokyo.proxy:3128"})
        page = context.new_page()
        response = page.request.get(EDGE_URL + "?region=Sevilla&category=Luxury")
        # EN: Check custom header or body for node info
        # ES: Verifica header personalizado o body para info de nodo
        # EO: Kontrolu propran header aŭ body por nodo-informo
        assert response.status == 200
        node = response.headers.get("X-Edge-Node", "")
        assert "asia" in node.lower()
        browser.close()
