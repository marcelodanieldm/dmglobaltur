import React, { useState, useEffect } from 'react';
import './ServiceControlPanel.css';

const SERVICES = [
  { key: 'vibe', name: 'Vibe-Matching' },
  { key: 'scarcity', name: 'Scarcity' },
  { key: 'reputation', name: 'Reputation Risk' }
];

export default function ServiceControlPanel() {
  const [insights, setInsights] = useState({});
  const [loading, setLoading] = useState(true);
  const [drawer, setDrawer] = useState(null);


  const fetchInsights = () => {
    setLoading(true);
    fetch('/api/v1/insights/unopened', {
      headers: { 'x-user-id': window.localStorage.getItem('user_id') || '' }
    })
      .then(r => r.json())
      .then(data => {
        const mapped = {};
        data.forEach(insight => {
          const key =
            insight.service_type === 'Vibe-Matching' ? 'vibe' :
            insight.service_type === 'Scarcity' ? 'scarcity' :
            insight.service_type === 'Reputation' ? 'reputation' : null;
          if (key && !mapped[key]) {
            mapped[key] = {
              main: insight.insight_title,
              details: insight.insight_body,
              sentiment: insight.insight_body?.sentiment_score || 0.5
            };
          }
        });
        setInsights(mapped);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchInsights();
  }, []);

  const getCardState = (service) => {
    if (loading) return 'loading';
    if (insights[service.key]?.sentiment < 0.4) return 'alert';
    return 'active';
  };

  // Marcar insight como abierto al abrir el Drawer
  const handleOpenDrawer = async (key) => {
    setDrawer(key);
    const insight = Object.entries(insights).find(([k]) => k === key)?.[1];
    if (insight && insight.details && insight.details.id) {
      await fetch('/api/v1/insights/mark_opened', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': window.localStorage.getItem('user_id') || ''
        },
        body: JSON.stringify({ insight_ids: [insight.details.id] })
      });
    }
  };

  return (
    <div className="scp-grid">
      {SERVICES.map(service => (
        <div
          key={service.key}
          className={`scp-card ${getCardState(service)}`}
          onClick={() => handleOpenDrawer(service.key)}
        >
          {getCardState(service) === 'loading' && <div className="scp-skeleton" />}
          {getCardState(service) === 'active' && (
            <>
              <h3>{service.name}</h3>
              <div className="scp-insight">{insights[service.key]?.main || 'Sin datos'}</div>
            </>
          )}
          {getCardState(service) === 'alert' && (
            <>
              <h3>{service.name}</h3>
              <div className="scp-alert">⚠️ Sentiment bajo</div>
              <div className="scp-insight">{insights[service.key]?.main || 'Sin datos'}</div>
            </>
          )}
        </div>
      ))}
      {drawer && (
        <div className="scp-drawer" onClick={() => { setDrawer(null); fetchInsights(); }}>
          <div className="scp-drawer-content" onClick={e => e.stopPropagation()}>
            <h2>{SERVICES.find(s => s.key === drawer).name}</h2>
            <pre>{JSON.stringify(insights[drawer]?.details, null, 2)}</pre>
            <button onClick={() => { setDrawer(null); fetchInsights(); }}>Cerrar</button>
          </div>
        </div>
      )}
    </div>
  );
}
