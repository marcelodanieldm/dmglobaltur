# Automated Test Suite Documentation

---

## ENGLISH

This project includes automated end-to-end tests for both the Xiaohongshu scraper and the FastAPI backend API.

### 1. Scraper Tests (Playwright, Pytest)
- Location: `tests/test_scraper_playwright.py`
- Validates browser launch, hashtag extraction, URL and sentiment integrity, and performance (<30s).
- Run with:
  ```bash
  pytest tests/test_scraper_playwright.py
  ```

### 2. API Tests (Pytest)
- Location: `tests/test_api_fastapi.py`
- Validates ingestion, retrieval, rate-limiting, and performance of the API.
- Run with:
  ```bash
  pytest tests/test_api_fastapi.py
  ```

### 3. Continuous Integration (GitHub Actions)
- Workflow: `.github/workflows/ci.yml`
- Runs all tests automatically on every push to `main`.

---

## ESPAÑOL

Este proyecto incluye pruebas automáticas end-to-end tanto para el scraper de Xiaohongshu como para la API backend FastAPI.

### 1. Pruebas del Scraper (Playwright, Pytest)
- Ubicación: `tests/test_scraper_playwright.py`
- Valida el lanzamiento del navegador, extracción de hashtags, integridad de URLs y sentimiento, y el rendimiento (<30s).
- Ejecuta con:
  ```bash
  pytest tests/test_scraper_playwright.py
  ```

### 2. Pruebas de la API (Pytest)
- Ubicación: `tests/test_api_fastapi.py`
- Valida la ingesta, consulta, limitación de tasa y rendimiento de la API.
- Ejecuta con:
  ```bash
  pytest tests/test_api_fastapi.py
  ```

### 3. Integración Continua (GitHub Actions)
- Workflow: `.github/workflows/ci.yml`
- Ejecuta todas las pruebas automáticamente en cada push a `main`.

---

## ESPERANTO

Ĉi tiu projekto inkluzivas aŭtomatajn fin-al-finajn testojn por la Xiaohongshu-scraper kaj la FastAPI-backend-API.

### 1. Scraper-Testoj (Playwright, Pytest)
- Loko: `tests/test_scraper_playwright.py`
- Validigas la lanĉon de la retumilo, ekstrakton de hashtagoj, integrecon de URL-oj kaj sentimon, kaj la rendimenton (<30s).
- Lanĉu per:
  ```bash
  pytest tests/test_scraper_playwright.py
  ```

### 2. API-Testoj (Pytest)
- Loko: `tests/test_api_fastapi.py`
- Validigas la enigon, ricevon, limigon de petfrekvenco kaj rendimenton de la API.
- Lanĉu per:
  ```bash
  pytest tests/test_api_fastapi.py
  ```

### 3. Daŭra Integriĝo (GitHub Actions)
- Laborfluo: `.github/workflows/ci.yml`
- Aŭtomate rulas ĉiujn testojn ĉe ĉiu push al `main`.
