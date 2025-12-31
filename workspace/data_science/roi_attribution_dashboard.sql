-- Dashboard de Atribución de ROI para el Cliente
-- Une api_calls, user_recommendations y client_sales_data
-- Mide ventas en 48h tras consumir un Scarcity Insight
-- Filtro por región (Europa vs Latam)

SELECT
  dmc.region,
  CASE WHEN r.recommendation_type = 'Scarcity Insight' THEN 'Con IA' ELSE 'Sin IA' END AS tipo_ia,
  COUNT(DISTINCT s.sale_id) AS ventas,
  SUM(s.amount) AS ingresos
FROM api_calls a
JOIN user_recommendations r ON a.user_id = r.user_id AND a.call_id = r.api_call_id
LEFT JOIN client_sales_data s ON r.user_id = s.user_id
  AND s.sale_time BETWEEN r.recommendation_time AND r.recommendation_time + INTERVAL '48 hours'
JOIN dmc ON s.dmc_id = dmc.id
WHERE s.sale_id IS NOT NULL
GROUP BY dmc.region, tipo_ia
ORDER BY dmc.region, tipo_ia;
