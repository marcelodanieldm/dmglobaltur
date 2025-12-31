import React, { useState, useEffect } from 'react';
import ServiceControlPanel from './ServiceControlPanel';
import './ServiceDeliveryLayer.css';

export default function ServiceDeliveryLayer({ user, apiKey, tier }) {
  // Simula caché de insights por 6h
  const [insights, setInsights] = useState(null);
  const [lastFetch, setLastFetch] = useState(null);

  useEffect(() => {
    const cached = window.localStorage.getItem('insights_cache');
    const cachedTime = window.localStorage.getItem('insights_cache_time');
    if (cached && cachedTime && Date.now() - Number(cachedTime) < 6 * 60 * 60 * 1000) {
      setInsights(JSON.parse(cached));
      setLastFetch(Number(cachedTime));
    } else {
      fetch('/api/v1/insights/unopened', {
        headers: { 'x-user-id': user.id }
      })
        .then(r => r.json())
        .then(data => {
          setInsights(data);
          window.localStorage.setItem('insights_cache', JSON.stringify(data));
          window.localStorage.setItem('insights_cache_time', Date.now().toString());
          setLastFetch(Date.now());
        });
    }
  }, [user.id]);

  // UI: Visual cards (reuse ServiceControlPanel)
  return (
    <div className="service-delivery-root">
      <ServiceControlPanel insightsOverride={insights} />
      {tier >= 3 && apiKey && (
        <div className="api-access">
          <h3>API Access</h3>
          <div className="api-key">{apiKey}</div>
          <a href="/api-docs" target="_blank" rel="noopener noreferrer">API Documentation (Swagger/Redoc)</a>
        </div>
      )}
    </div>
  );
}
