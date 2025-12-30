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
from pydantic import BaseModel

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

# ─────────────────────────────────────────────
# BUSINESS MODELS / MODELOS DE NEGOCIO / KOMERCAJ MODELOJ
# ─────────────────────────────────────────────

class Revenue(Base):
    """
    EN: Gross revenue records for the business.
    ES: Registros de ingresos brutos del negocio.
    EO: Brutaj enspezaj registroj por la komerco.
    """
    __tablename__ = "revenue"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    region: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)

class Cost(Base):
    """
    EN: Operating costs (API tokens, proxies, cloud hosting).
    ES: Costos operativos (tokens API, proxies, cloud hosting).
    EO: Operaciaj kostoj (API-ĵetonoj, prokuriloj, nubo).
    """
    __tablename__ = "cost"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)  # e.g. 'api_token', 'proxy', 'cloud'
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    region: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)

class User(Base):
    """
    EN: User records for churn and break-even analytics.
    ES: Registros de usuarios para churn y equilibrio.
    EO: Uzantaj registroj por forlaso kaj ekvilibro.
    """
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region: Mapped[str] = mapped_column(Text, nullable=False)
    tier: Mapped[str] = mapped_column(Text, nullable=False)  # e.g. 'basic', 'pro', 'enterprise'
    is_active: Mapped[bool] = mapped_column(Integer, nullable=False, default=1)
    last_active: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)

class Client(Base):
    """
    EN: Client records for VIP/enterprise support.
    ES: Registros de clientes para soporte VIP/enterprise.
    EO: Klientaj registroj por VIP/enterprise subteno.
    """
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    tier: Mapped[str] = mapped_column(Text, nullable=False)
    usage: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_active: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)

class Churn(Base):
    """
    EN: Churn analytics records (user lost, region, date).
    ES: Registros de churn (usuario perdido, región, fecha).
    EO: Forlasaj analizaj registroj (uzanto perdita, regiono, dato).
    """
    __tablename__ = "churn"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    region: Mapped[str] = mapped_column(Text, nullable=False)
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

# Revenue
class RevenueIn(BaseModel):
    amount: float
    region: str

@app.post("/api/v1/business/revenue", status_code=201, dependencies=[Depends(get_api_key)])
async def add_revenue(data: RevenueIn, request: Request):
    """
    EN: Add a gross revenue record.
    ES: Agrega un registro de ingreso bruto.
    EO: Aldonu brutenspezan registron.
    """
    async with SessionLocal() as session:
        rev = Revenue(amount=data.amount, region=data.region)
        session.add(rev)
        await session.commit()
    return {"status": "success"}

@app.get("/api/v1/business/revenue", dependencies=[Depends(get_api_key)])
async def get_revenue(region: str = None):
    """
    EN: Get gross revenue records (optionally filtered by region).
    ES: Obtiene registros de ingresos brutos (opcional por región).
    EO: Ricevu brutenspezajn registrojn (laŭregiona filtrado).
    """
    async with SessionLocal() as session:
        q = select(Revenue)
        if region:
            q = q.where(Revenue.region == region)
        result = await session.execute(q)
        return [dict(id=r.id, amount=r.amount, region=r.region, timestamp=r.timestamp.isoformat()) for r in result.scalars().all()]

# Cost
class CostIn(BaseModel):
    type: str
    amount: float
    region: str

@app.post("/api/v1/business/cost", status_code=201, dependencies=[Depends(get_api_key)])
async def add_cost(data: CostIn, request: Request):
    """
    EN: Add an operating cost record.
    ES: Agrega un registro de costo operativo.
    EO: Aldonu operacikostan registron.
    """
    async with SessionLocal() as session:
        cost = Cost(type=data.type, amount=data.amount, region=data.region)
        session.add(cost)
        await session.commit()
    return {"status": "success"}

@app.get("/api/v1/business/cost", dependencies=[Depends(get_api_key)])
async def get_cost(region: str = None):
    """
    EN: Get operating cost records (optionally filtered by region).
    ES: Obtiene registros de costos operativos (opcional por región).
    EO: Ricevu operacikostajn registrojn (laŭregiona filtrado).
    """
    async with SessionLocal() as session:
        q = select(Cost)
        if region:
            q = q.where(Cost.region == region)
        result = await session.execute(q)
        return [dict(id=r.id, type=r.type, amount=r.amount, region=r.region, timestamp=r.timestamp.isoformat()) for r in result.scalars().all()]

# User
class UserIn(BaseModel):
    region: str
    tier: str
    is_active: int = 1

@app.post("/api/v1/business/user", status_code=201, dependencies=[Depends(get_api_key)])
async def add_user(data: UserIn, request: Request):
    """
    EN: Add a user record.
    ES: Agrega un registro de usuario.
    EO: Aldonu uzantregistaron.
    """
    async with SessionLocal() as session:
        user = User(region=data.region, tier=data.tier, is_active=data.is_active)
        session.add(user)
        await session.commit()
    return {"status": "success"}

@app.get("/api/v1/business/user", dependencies=[Depends(get_api_key)])
async def get_users(region: str = None, tier: str = None):
    """
    EN: Get user records (optionally filtered by region/tier).
    ES: Obtiene registros de usuarios (opcional por región/tier).
    EO: Ricevu uzantregistrojn (laŭregiona/tier filtrado).
    """
    async with SessionLocal() as session:
        q = select(User)
        if region:
            q = q.where(User.region == region)
        if tier:
            q = q.where(User.tier == tier)
        result = await session.execute(q)
        return [dict(id=u.id, region=u.region, tier=u.tier, is_active=u.is_active, last_active=u.last_active.isoformat()) for u in result.scalars().all()]

# Client
class ClientIn(BaseModel):
    name: str
    tier: str
    usage: int = 0

@app.post("/api/v1/business/client", status_code=201, dependencies=[Depends(get_api_key)])
async def add_client(data: ClientIn, request: Request):
    """
    EN: Add a client record.
    ES: Agrega un registro de cliente.
    EO: Aldonu klientregistaron.
    """
    async with SessionLocal() as session:
        client = Client(name=data.name, tier=data.tier, usage=data.usage)
        session.add(client)
        await session.commit()
    return {"status": "success"}

@app.get("/api/v1/business/client", dependencies=[Depends(get_api_key)])
async def get_clients(tier: str = None):
    """
    EN: Get client records (optionally filtered by tier).
    ES: Obtiene registros de clientes (opcional por tier).
    EO: Ricevu klientregistrojn (laŭtier filtrado).
    """
    async with SessionLocal() as session:
        q = select(Client)
        if tier:
            q = q.where(Client.tier == tier)
        result = await session.execute(q)
        return [dict(id=c.id, name=c.name, tier=c.tier, usage=c.usage, last_active=c.last_active.isoformat()) for c in result.scalars().all()]

# Churn
class ChurnIn(BaseModel):
    user_id: int
    region: str

@app.post("/api/v1/business/churn", status_code=201, dependencies=[Depends(get_api_key)])
async def add_churn(data: ChurnIn, request: Request):
    """
    EN: Add a churn record (user lost).
    ES: Agrega un registro de churn (usuario perdido).
    EO: Aldonu forlasan registron (uzanto perdita).
    """
    async with SessionLocal() as session:
        churn = Churn(user_id=data.user_id, region=data.region)
        session.add(churn)
        await session.commit()
    return {"status": "success"}

@app.get("/api/v1/business/churn", dependencies=[Depends(get_api_key)])
async def get_churn(region: str = None):
    """
    EN: Get churn records (optionally filtered by region).
    ES: Obtiene registros de churn (opcional por región).
    EO: Ricevu forlasajn registrojn (laŭregiona filtrado).
    """
    async with SessionLocal() as session:
        q = select(Churn)
        if region:
            q = q.where(Churn.region == region)
        result = await session.execute(q)
        return [dict(id=ch.id, user_id=ch.user_id, region=ch.region, timestamp=ch.timestamp.isoformat()) for ch in result.scalars().all()]

# ─────────────────────────────────────────────────────────────
# RUN: uvicorn main:app --reload
# ─────────────────────────────────────────────────────────────
