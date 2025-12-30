"""
main.py
=======

─────────────────────────────────────────────────────────────
DOCUMENTATION IN ENGLISH
─────────────────────────────────────────────────────────────

This FastAPI backend exposes and stores Xiaohongshu luxury travel trend data for DM Global Tur.

Features:
- PostgreSQL (Supabase) integration via SQLAlchemy (async).
- API endpoints for ingesting and retrieving trend data.
- Rate limiting and API key authentication for secure access.
- Auto-generated API documentation (Swagger UI).

─────────────────────────────────────────────────────────────
DOCUMENTACIÓN EN ESPAÑOL
─────────────────────────────────────────────────────────────

Este backend FastAPI expone y almacena datos de tendencias de viajes de lujo de Xiaohongshu para DM Global Tur.

Características:
- Integración con PostgreSQL (Supabase) usando SQLAlchemy (async).
- Endpoints API para ingresar y consultar datos de tendencias.
- Limitación de tasa y autenticación por API key para acceso seguro.
- Documentación automática de la API (Swagger UI).

─────────────────────────────────────────────────────────────
DOCUMENTADO EN ESPERANTO
─────────────────────────────────────────────────────────────

Ĉi tiu FastAPI-backend publikigas kaj konservas tendencajn datumojn pri luksaj vojaĝoj el Xiaohongshu por DM Global Tur.

Trajtoj:
- PostgreSQL (Supabase) integriĝo per SQLAlchemy (async).
- API-finoj por enigi kaj ricevi tendencajn datumojn.
- Limigo de petfrekvenco kaj API-ŝlosila aŭtentikigo por sekura aliro.
- Aŭtomate generita API-dokumentado (Swagger UI).
"""

import os
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, desc
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Integer, Float, Text, TIMESTAMP
from starlette.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# ─────────────────────────────────────────────────────────────
# CONFIGURATION / CONFIGURACIÓN / AGORDO
# ─────────────────────────────────────────────────────────────

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/dbname")
API_KEY = os.getenv("API_KEY", "changeme")

# ─────────────────────────────────────────────────────────────
# DATABASE SETUP / CONFIGURACIÓN DE BASE DE DATOS / DATUMBANKO
# ─────────────────────────────────────────────────────────────

Base = declarative_base()

class XiaohongshuTrend(Base):
    __tablename__ = "xiaohongshu_trends"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hashtag: Mapped[str] = mapped_column(Text, nullable=False)
    post_count: Mapped[int] = mapped_column(Integer, nullable=False)
    sample_posts: Mapped[list] = mapped_column(JSONB, nullable=False)
    avg_sentiment: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# ─────────────────────────────────────────────────────────────
# FASTAPI APP / APLICACIÓN FASTAPI / FASTAPI-APLIKAĴO
# ─────────────────────────────────────────────────────────────

app = FastAPI(title="DM Global Tur Xiaohongshu Trends API",
              description="API for storing and serving Xiaohongshu luxury travel trend data.",
              version="1.0.0")

# CORS (opcional, ajusta según necesidades)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# API Key Auth
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return api_key

# ─────────────────────────────────────────────────────────────
# ENDPOINTS / ENDPOINTS / FINOJ
# ─────────────────────────────────────────────────────────────

@app.post("/api/v1/ingest/xiaohongshu", status_code=201)
async def ingest_xiaohongshu(data: List[dict], request: Request):
    """
    EN: Ingest Xiaohongshu trend data (list of dicts) into the database.
    ES: Ingesta datos de tendencias de Xiaohongshu (lista de diccionarios) en la base de datos.
    EO: Enigu tendencajn datumojn de Xiaohongshu (listo de vortaro) en la datumbazon.
    """
    async with SessionLocal() as session:
        for item in data:
            trend = XiaohongshuTrend(
                hashtag=item["hashtag"],
                post_count=item["post_count"],
                sample_posts=item["sample_posts"],
                avg_sentiment=item["avg_sentiment"],
                timestamp=datetime.now(timezone.utc)
            )
            session.add(trend)
        await session.commit()
    return {"status": "success"}

@app.get("/api/v1/trends/xiaohongshu", dependencies=[Depends(get_api_key)])
@limiter.limit("100/minute")
async def get_xiaohongshu_trends(request: Request):
    """
    EN: Get the latest 10 Xiaohongshu trending hashtags from the database.
    ES: Obtiene los últimos 10 hashtags de tendencia de Xiaohongshu desde la base de datos.
    EO: Ricevu la lastajn 10 tendencajn hashtagojn de Xiaohongshu el la datumbazo.
    """
    async with SessionLocal() as session:
        result = await session.execute(
            select(XiaohongshuTrend).order_by(desc(XiaohongshuTrend.timestamp)).limit(10)
        )
        trends = result.scalars().all()
        return [
            {
                "id": t.id,
                "hashtag": t.hashtag,
                "post_count": t.post_count,
                "sample_posts": t.sample_posts,
                "avg_sentiment": t.avg_sentiment,
                "timestamp": t.timestamp.isoformat()
            }
            for t in trends
        ]

@app.get("/health")
async def health():
    """
    EN: Health check endpoint.
    ES: Endpoint de verificación de salud.
    EO: Fino por sanstato-kontrolo.
    """
    return {"status": "ok"}

# ─────────────────────────────────────────────────────────────
# RUN: uvicorn main:app --reload
# ─────────────────────────────────────────────────────────────
