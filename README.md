# DM Global Tur

---

## ENGLISH

DM Global Tur is a multilingual SaaS for analyzing and visualizing luxury travel trends from Xiaohongshu (Little Red Book). It now features a fully integrated, real-time forecasting dashboard and CEO business logic dashboard, with secure API Key authentication and multilingual UI/documentation (EN/ES/EO).

### Key Features (2025)
- Dynamic Forecasting Dashboard: Predictive map, trend comparison, global footprint, mobile alerts ([details](frontend/README_DASHBOARD_FORECASTING.md))
- CEO Account Dashboard: Financial control, break-even, VIP support, scaling metrics ([details](frontend/README_CEO_ACCOUNT.md))
- FastAPI backend with PostgreSQL (Supabase-ready)
- Secure API Key authentication for all endpoints
- Multilingual UI and documentation (English, Spanish, Esperanto)
- End-to-end encryption for sensitive data (inventory)
- Automated tests and CI/CD

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
5. Open `frontend/dashboard_forecasting.html` or `frontend/ceo_account.html` in your browser.

---

## ESPAÑOL

DM Global Tur es una plataforma SaaS multilingüe para analizar y visualizar tendencias de viajes de lujo desde Xiaohongshu. Ahora incluye dashboard de forecasting en tiempo real y dashboard financiero para CEO, con autenticación segura por API Key y documentación/UI en EN/ES/EO.

### Novedades (2025)
- Dashboard de Forecasting: Mapa predictivo, comparación de tendencias, huella global, alertas móviles ([detalles](frontend/README_DASHBOARD_FORECASTING.md))
- Dashboard CEO: Control financiero, equilibrio, soporte VIP, métricas de escalado ([detalles](frontend/README_CEO_ACCOUNT.md))
- Backend FastAPI con PostgreSQL (Supabase)
- Autenticación segura por API Key
- UI y documentación multilingüe (inglés, español, esperanto)
- Cifrado de extremo a extremo para datos sensibles
- Pruebas automáticas y CI/CD

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
5. Abre `frontend/dashboard_forecasting.html` o `frontend/ceo_account.html` en tu navegador.

---

## ESPERANTO

DM Global Tur estas plurlingva SaaS por analizi kaj vizualigi luksajn vojaĝajn tendencojn el Xiaohongshu. Nun inkluzivas prognozan dashboard-on en reala tempo kaj CEO-financan panelon, kun sekura API-ŝlosila aŭtentikigo kaj dokumentado/UI en EN/ES/EO.

### Novaĵoj (2025)
- Prognoza Dashboard: Prognoza mapo, tendenca komparo, tutmonda spuro, poŝtelefonaj atentigoj ([detaloj](frontend/README_DASHBOARD_FORECASTING.md))
- CEO-Panelo: Financa kontrolo, ekvilibro, VIP-subteno, skalaj metrikoj ([detaloj](frontend/README_CEO_ACCOUNT.md))
- FastAPI-backend kun PostgreSQL (Supabase)
- Sekura API-ŝlosila aŭtentikigo
- Plurlingva UI kaj dokumentado (angla, hispana, esperanto)
- Fina-ĉifrado por sentemaj datumoj
- Aŭtomataj testoj kaj CI/CD

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
5. Malfermu `frontend/dashboard_forecasting.html` aŭ `frontend/ceo_account.html` en via retumilo.

---

## Documentation
- [Forecasting Dashboard](frontend/README_DASHBOARD_FORECASTING.md)
- [CEO Account Dashboard](frontend/README_CEO_ACCOUNT.md)
- [Frontend Overview](frontend/README_FRONTEND.md)
- [Backend Overview](README_BACKEND.md)
- [QA & Stress Testing](tests/README_QA_STRESS.md)

---

## License
MIT
