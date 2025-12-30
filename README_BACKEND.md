# DM Global Tur FastAPI Backend

---

## ENGLISH

### 1. Installation

1. Clone the repository and enter the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements-backend.txt
   ```
3. Set up your environment variables (DATABASE_URL, API_KEY) in a `.env` file or your system.
4. Install and configure PostgreSQL (Supabase or local).

### 2. Database Migration

1. Initialize Alembic (if not already):
   ```bash
   alembic upgrade head
   ```

### 3. Running the API

```bash
uvicorn main:app --reload
```

- Access the API docs at: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 4. Endpoints
- `POST /api/v1/ingest/xiaohongshu` — Ingest trend data (from scraper)
- `GET /api/v1/trends/xiaohongshu` — Get latest 10 trends (API key required, rate-limited)

---

## ESPAÑOL

### 1. Instalación

1. Clona el repositorio y entra en la carpeta del proyecto.
2. Instala las dependencias:
   ```bash
   pip install -r requirements-backend.txt
   ```
3. Configura las variables de entorno (DATABASE_URL, API_KEY) en un archivo `.env` o en tu sistema.
4. Instala y configura PostgreSQL (Supabase o local).

### 2. Migración de Base de Datos

1. Inicializa Alembic (si no está hecho):
   ```bash
   alembic upgrade head
   ```

### 3. Ejecutar la API

```bash
uvicorn main:app --reload
```

- Documentación de la API: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 4. Endpoints
- `POST /api/v1/ingest/xiaohongshu` — Ingesta de datos de tendencias (desde el scraper)
- `GET /api/v1/trends/xiaohongshu` — Consulta de las 10 últimas tendencias (requiere API key, limitado por IP)

---

## ESPERANTO

### 1. Instalado

1. Klonu la deponejon kaj eniru la projektdosierujon.
2. Instalu dependecojn:
   ```bash
   pip install -r requirements-backend.txt
   ```
3. Agordu la medivariablojn (DATABASE_URL, API_KEY) en `.env` aŭ via sistemo.
4. Instalu kaj agordu PostgreSQL (Supabase aŭ loka).

### 2. Datumbaza Migrado

1. Inicializu Alembic (se necese):
   ```bash
   alembic upgrade head
   ```

### 3. Lanĉi la API

```bash
uvicorn main:app --reload
```

- API-dokumentado: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 4. Finoj
- `POST /api/v1/ingest/xiaohongshu` — Enigo de tendencaj datumoj (el scraper)
- `GET /api/v1/trends/xiaohongshu` — Ricevu la 10 lastajn tendencojn (postulas API-ŝlosilon, limigita per IP)
