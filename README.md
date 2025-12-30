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
- `frontend/` — Landing page & dashboard
- `notebooks/` — Data analysis notebooks
- `tests/` — Automated tests
- `.github/workflows/` — CI/CD pipelines

---

## License
MIT
