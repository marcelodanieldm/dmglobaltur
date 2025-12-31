# Data Science & BI - DM Global Tur

## 1. Vibe-Matching Classifier (Python + Gemini 1.5 Pro)
- `vibe_matching_classifier.py`: Clasifica perfiles de turistas de lujo en 5 arquetipos, usando IA generativa.
- Entrada: texto de reseñas/posts. Salida: arquetipo, confidence score, cultural triggers.

## 2. Scarcity Opportunity Detector (Python + Pandas)
- `scarcity_opportunity_detector.py`: Cruza inventario local y demanda China, calcula OpportunityIndex y alerta si > 0.8.
- Optimizado para 10,000 SKUs en <5s.

## 3. SQL para Analistas de Datos
- `roi_attribution_dashboard.sql`: Consulta para atribución de ROI tras consumir insights, lista ventas e ingresos con/sin IA, filtro por región.
- `ltv_churn_business_health.sql`: Vista para LTV, churn mensual, costos operativos, break-even y reporte semanal de servicios más rentables.

## Reglas de negocio
- Velocidad: <15 minutos de captura a dashboard.
- Integridad: Validación QA con Golden Records.
- Privacidad: Sin datos personales de ciudadanos chinos (solo tendencias y metadatos).
