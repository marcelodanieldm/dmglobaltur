-- 1. EXTENSIONES Y SEGURIDAD
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. TABLA DE USUARIOS Y SUSCRIPCIONES (CORE)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    country_code VARCHAR(3) NOT NULL, -- ISO 3166-1 alpha-3 (ESP, ARG, CHN, etc.)
    tier_id INTEGER DEFAULT 0, -- 0: Free, 1: Explorer, 2: Strategist, 3: Emperor
    stripe_customer_id TEXT,
    subscription_status TEXT DEFAULT 'inactive', -- active, past_due, canceled
    api_key TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. TABLA DE TENDENCIAS DE MERCADO (INGESTA DESDE CHINA)
-- Esta tabla almacena lo que el Data Scientist extrae de Xiaohongshu/Ctrip
CREATE TABLE market_trends (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_platform TEXT NOT NULL, -- 'Xiaohongshu', 'Weibo', 'Ctrip'
    hashtag_or_keyword TEXT NOT NULL,
    sentiment_score FLOAT, -- De -1.0 a 1.0
    virality_velocity FLOAT, -- Velocidad de crecimiento de menciones
    raw_content_summary TEXT, -- Resumen del contenido en Mandarín
    translated_content TEXT, -- Traducción al inglés/español vía Gemini
    detected_arquetype TEXT, -- 'Old Money', 'New Rich', etc.
    target_region VARCHAR(3), -- A qué país/región afecta esta tendencia
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. TABLA DE RECOMENDACIONES PERSONALIZADAS (EL "PRODUCTO")
-- Aquí se guardan los insights generados para cada cliente específico
CREATE TABLE client_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    service_type TEXT NOT NULL, -- 'Vibe-Matching', 'Scarcity', 'Reputation'
    insight_title TEXT NOT NULL,
    insight_body JSONB NOT NULL, -- Recomendación estructurada (To-do, Never-do)
    opportunity_score INTEGER, -- 0 a 100
    is_critical BOOLEAN DEFAULT FALSE,
    delivered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    was_opened BOOLEAN DEFAULT FALSE
);

-- 5. TABLA DE INVENTARIO LOCAL (RETAIL/RENTADORAS)
-- Para el servicio de Scarcity, cruzamos esto con market_trends
CREATE TABLE client_inventory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    sku_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    current_stock INTEGER DEFAULT 0,
    price_local NUMERIC(10, 2),
    last_update TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. TABLA DE LOGS DE IA Y COSTOS (DANIEL / CEO)
CREATE TABLE ai_usage_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    model_name TEXT DEFAULT 'gemini-1.5-flash',
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_cost NUMERIC(10, 6), -- Costo real en USD de la llamada
    called_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. TABLA DE LOGS DE SALUD DEL SISTEMA (CIRCUIT BREAKER, FALLAS DE FUENTE)
CREATE TABLE system_health_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    source TEXT NOT NULL, -- XHS_Scraper, Ctrip_API, Baidu_Mirror
    event TEXT NOT NULL, -- circuit_break, recovery, error
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
