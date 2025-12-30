# DM Global Tur

---

## ENGLISH

DM Global Tur is a multilingual platform for analyzing and visualizing luxury travel trends from Xiaohongshu (Little Red Book). It includes a robust data pipeline, backend API, frontend dashboard, automated tests, and documentation in English, Spanish, and Esperanto.

### Features
- Automated web scraper (Playwright, Python)
- FastAPI backend with PostgreSQL (Supabase-ready)
- Frontend landing page and dashboard (HTML/CSS/JS)
- Data analysis notebooks (Jupyter, Pandas, Matplotlib, Seaborn)
- End-to-end tests and CI/CD (GitHub Actions)
- Multilingual documentation and UI

### Quick Start
1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-backend.txt
   ```
2. Set up your `.env` (see `.env.example`).
3. Run Alembic migrations:
   ```bash
   alembic upgrade head
   ```
4. Start the backend:
   ```bash
   uvicorn main:app --reload
   ```
5. Open `frontend/index.html` in your browser.

---

## ESPAÑOL

DM Global Tur es una plataforma multilingüe para analizar y visualizar tendencias de viajes de lujo desde Xiaohongshu. Incluye un pipeline de datos robusto, API backend, dashboard frontend, pruebas automáticas y documentación en inglés, español y esperanto.

### Características
- Scraper web automatizado (Playwright, Python)
- Backend FastAPI con PostgreSQL (compatible con Supabase)
- Landing page y dashboard frontend (HTML/CSS/JS)
- Notebooks de análisis de datos (Jupyter, Pandas, Matplotlib, Seaborn)
- Pruebas end-to-end y CI/CD (GitHub Actions)
- Documentación y UI multilingüe

### Inicio Rápido
1. Clona el repositorio e instala dependencias:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-backend.txt
   ```
2. Configura tu `.env` (ver `.env.example`).
3. Ejecuta las migraciones Alembic:
   ```bash
   alembic upgrade head
   ```
4. Inicia el backend:
   ```bash
   uvicorn main:app --reload
   ```
5. Abre `frontend/index.html` en tu navegador.

---

## ESPERANTO

DM Global Tur estas plurlingva platformo por analizi kaj vizualigi luksajn vojaĝajn tendencojn el Xiaohongshu. Ĝi inkluzivas fortikan datuman pipeline, backend-API, frontend-dashboard, aŭtomatajn testojn kaj dokumentadon en la angla, hispana kaj Esperanto.

### Trajtoj
- Aŭtomata retumila scraper (Playwright, Python)
- FastAPI-backend kun PostgreSQL (Supabase-preta)
- Surteriĝa paĝo kaj dashboard (HTML/CSS/JS)
- Datum-analizaj notlibroj (Jupyter, Pandas, Matplotlib, Seaborn)
- Fin-al-finaj testoj kaj CI/CD (GitHub Actions)
- Plurlingva dokumentado kaj UI

### Rapida Komenco
1. Klonu la deponejon kaj instalu dependecojn:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-backend.txt
   ```
2. Agordu vian `.env` (vidu `.env.example`).
3. Rulu Alembic-migradojn:
   ```bash
   alembic upgrade head
   ```
4. Lanĉu la backend:
   ```bash
   uvicorn main:app --reload
   ```
5. Malfermu `frontend/index.html` en via retumilo.

---

## Project Structure / Estructura / Strukturo

- `xiaohongshu_scraper.py` — Scraper script
- `main.py` — FastAPI backend
- `recommendation_api.py` — Recommendation endpoints (Vibe-Matching, Scarcity, JWT, Redis)
- `intelligence_engine.py` — Multilingual sentiment, intent, persona & expectation-gap engine
- `frontend/` — Landing page & dashboard
- `notebooks/` — Data analysis notebooks
- `tests/` — Automated tests (scraper, API, recommendation logic)
- `.github/workflows/` — CI/CD pipelines

---

## API Endpoints / Endpoints de API / API-Finoj

### ENGLISH
- `/api/v1/ingest/xiaohongshu` (POST): Ingest trend data (JSON)
- `/api/v1/trends/xiaohongshu` (GET): Get latest 10 trends (API key, rate-limited)
- `/api/v1/recommend/vibe-matching` (GET, JWT): Recommend 3 activities in destination based on persona and sentiment
- `/api/v1/recommend/scarcity` (GET, JWT): Return items with low stock in China but high in destination

### ESPAÑOL
- `/api/v1/ingest/xiaohongshu` (POST): Ingesta de datos de tendencias (JSON)
- `/api/v1/trends/xiaohongshu` (GET): Consulta de las 10 últimas tendencias (API key, limitado)
- `/api/v1/recommend/vibe-matching` (GET, JWT): Recomienda 3 actividades en el destino según persona y sentimiento
- `/api/v1/recommend/scarcity` (GET, JWT): Devuelve artículos con poco stock en China y alto en el destino

### ESPERANTO
- `/api/v1/ingest/xiaohongshu` (POST): Enigo de tendencaj datumoj (JSON)
- `/api/v1/trends/xiaohongshu` (GET): Ricevu la 10 lastajn tendencojn (API-ŝlosilo, limigita)
- `/api/v1/recommend/vibe-matching` (GET, JWT): Rekomendu 3 agadojn en la celo laŭ persono kaj sentimo
- `/api/v1/recommend/scarcity` (GET, JWT): Redonu varojn kun malmulta stoko en Ĉinio sed multe en la celo

---

## Recommendation Logic / Lógica de Recomendación / Rekomenda Logiko

### ENGLISH
- Vibe-Matching: Suggests activities based on user persona, destination, and current Chinese sentiment.
- Scarcity: Returns luxury items with low stock in China but high in the destination (mock inventory).
- Geo-Fencing: Prioritizes South American data if user is in Brazil/LatAm.
- Redis caching for fast responses (<500ms).
- JWT authentication for secure, tiered access.

### ESPAÑOL
- Vibe-Matching: Sugiere actividades según la persona, destino y sentimiento chino actual.
- Escasez: Devuelve artículos de lujo con poco stock en China y alto en el destino (inventario simulado).
- Geo-Fencing: Prioriza datos sudamericanos si el usuario está en Brasil/LatAm.
- Caché Redis para respuestas rápidas (<500ms).
- Autenticación JWT para acceso seguro y por nivel.

### ESPERANTO
- Vibe-Matching: Sugestas agadojn laŭ persono, celo kaj aktuala ĉina sentimo.
- Malabundo: Redonas luksajn varojn kun malmulta stoko en Ĉinio kaj multe en la celo (simulita inventaro).
- Geo-Fencing: Prioritatigas sudamerikajn datumojn se uzanto estas en Brazilo/LatAm.
- Redis-kaŝmemoro por rapidaj respondoj (<500ms).
- JWT-aŭtentikigo por sekura, tavoligita aliro.

---

## QA & Testing / QA y Pruebas / QA kaj Testado

### ENGLISH
- Automated tests for scraper, API, and recommendation logic (cultural, language, performance).
- CI/CD pipeline runs all tests on every push.

### ESPAÑOL
- Pruebas automáticas para scraper, API y lógica de recomendación (cultural, idioma, rendimiento).
- CI/CD ejecuta todas las pruebas en cada push.

### ESPERANTO
- Aŭtomataj testoj por scraper, API kaj rekomenda logiko (kultura, lingva, rendimento).
- CI/CD rulas ĉiujn testojn ĉe ĉiu push.

---

## Iteration History / Historial de Iteraciones / Iteracia Historio

### ENGLISH
- Initial project setup: scraper, backend API, frontend, notebooks, tests, CI/CD.
- Added multilingual documentation and UI (EN/ES/EO).
- Implemented Playwright-based Xiaohongshu scraper with Gemini 1.5 Flash API for sentiment.
- Developed FastAPI backend with PostgreSQL, endpoints for data ingestion and trends.
- Created Alembic migrations and database schema.
- Built frontend landing page and dashboard (HTML/CSS/JS, responsive, multilingual).
- Added automated tests for scraper, API, and recommendation logic (Pytest, Playwright).
- Integrated GitHub Actions for CI/CD.
- Implemented intelligence_engine.py for sentiment, intent, persona, and expectation-gap enrichment.
- Developed recommendation_api.py with Vibe-Matching, Scarcity, JWT, Redis, and geo-fencing.
- Added QA and integration tests for cultural logic, localization, and access control.

### ESPAÑOL
- Configuración inicial del proyecto: scraper, API backend, frontend, notebooks, pruebas, CI/CD.
- Documentación y UI multilingüe (EN/ES/EO).
- Scraper Xiaohongshu con Playwright y análisis de sentimiento Gemini 1.5 Flash API.
- Backend FastAPI con PostgreSQL, endpoints para ingesta y consulta de tendencias.
- Migraciones Alembic y esquema de base de datos.
- Landing page y dashboard frontend (HTML/CSS/JS, responsivo, multilingüe).
- Pruebas automáticas para scraper, API y lógica de recomendación (Pytest, Playwright).
- Integración de CI/CD con GitHub Actions.
- intelligence_engine.py para enriquecimiento de sentimiento, intención, persona y expectation-gap.
- recommendation_api.py con Vibe-Matching, Escasez, JWT, Redis y geo-fencing.
- Pruebas de QA e integración para lógica cultural, localización y control de acceso.

### ESPERANTO
- Komenca agordo de la projekto: scraper, backend-API, frontend, notlibroj, testoj, CI/CD.
- Plurlingva dokumentado kaj UI (EN/ES/EO).
- Xiaohongshu-scraper per Playwright kaj sentimanalyzo per Gemini 1.5 Flash API.
- FastAPI-backend kun PostgreSQL, finoj por enigo kaj tendencoj.
- Alembic-migradoj kaj datumbaza skemo.
- Surteriĝa paĝo kaj dashboard (HTML/CSS/JS, respondema, plurlingva).
- Aŭtomataj testoj por scraper, API kaj rekomenda logiko (Pytest, Playwright).
- CI/CD integriĝo per GitHub Actions.
- intelligence_engine.py por sentimo, intenco, persono kaj expectation-gap riĉigo.
- recommendation_api.py kun Vibe-Matching, Malabundo, JWT, Redis kaj geo-fencing.
- QA kaj integriĝaj testoj por kultura logiko, lokalizado kaj alirkontrolo.

---

## License
MIT
