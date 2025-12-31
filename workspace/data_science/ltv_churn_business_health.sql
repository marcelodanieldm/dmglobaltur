-- Vista de Salud del Negocio: LTV, Churn, Costos y Break-even
CREATE OR REPLACE VIEW business_health AS
SELECT
  u.user_id,
  DATE_TRUNC('month', s.sale_time) AS mes,
  COUNT(DISTINCT s.sale_id) AS ventas,
  SUM(s.amount) AS ingresos,
  SUM(g.tokens * g.token_cost + i.infra_cost) AS costo_operativo,
  SUM(s.amount) / NULLIF(SUM(g.tokens * g.token_cost + i.infra_cost),0) AS break_even,
  COUNT(DISTINCT CASE WHEN u.cancelled_at IS NOT NULL AND DATE_TRUNC('month', u.cancelled_at) = DATE_TRUNC('month', s.sale_time) THEN u.user_id END) AS churned,
  COUNT(DISTINCT u.user_id) AS total_users,
  (SUM(s.amount) / NULLIF(COUNT(DISTINCT u.user_id),0)) AS ltv,
  (COUNT(DISTINCT CASE WHEN u.cancelled_at IS NOT NULL AND DATE_TRUNC('month', u.cancelled_at) = DATE_TRUNC('month', s.sale_time) THEN u.user_id END)::float / NULLIF(COUNT(DISTINCT u.user_id),0)) AS churn_rate
FROM users u
LEFT JOIN client_sales_data s ON u.user_id = s.user_id
LEFT JOIN gemini_usage g ON u.user_id = g.user_id AND DATE_TRUNC('month', g.usage_time) = DATE_TRUNC('month', s.sale_time)
LEFT JOIN infra_costs i ON DATE_TRUNC('month', i.cost_time) = DATE_TRUNC('month', s.sale_time)
GROUP BY u.user_id, mes;

-- Reporte semanal: top 5 servicios más rentables
SELECT service, SUM(amount) AS ingresos
FROM client_sales_data
WHERE sale_time >= NOW() - INTERVAL '7 days'
GROUP BY service
ORDER BY ingresos DESC
LIMIT 5;
