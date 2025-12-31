# Ejemplo de uso SQL

## ROI Attribution Dashboard

```sql
-- Ejecuta en Supabase SQL editor
\i roi_attribution_dashboard.sql
```

- Visualiza los resultados en Chart.js usando los campos: region, tipo_ia, ventas, ingresos.

## Business Health View

```sql
-- Ejecuta en Supabase SQL editor
\i ltv_churn_business_health.sql
```

- Consulta la vista business_health para obtener LTV, churn y costos por usuario/mes.
- Ejecuta el reporte semanal para ver el top 5 de servicios más rentables.
