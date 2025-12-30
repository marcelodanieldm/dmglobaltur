// Forecasting & Global Trends Dashboard Logic
// EN / ES / EO

// --- Predictive Map (Leaflet + Glow) ---
// EN: Fetch viral velocity data from backend. ES: Consulta datos de velocidad viral del backend. EO: Ricevu datumojn pri vira rapideco de la backend.
const API_BASE = 'http://localhost:8000/api/v1';
const API_KEY = localStorage.getItem('dmgt_api_key') || prompt('Enter API Key for dashboard:');

function fetchAuth(url) {
  return fetch(url, { headers: { 'X-API-Key': API_KEY } }).then(r => r.json());
}

const map = L.map('predictive-map').setView([20, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// EN: Get latest trends and plot as viral velocity. ES: Obtiene tendencias y grafica como velocidad viral. EO: Ricevu tendencojn kaj montru kiel vira rapideco.
fetchAuth(`${API_BASE}/trends/xiaohongshu`).then(trends => {
  trends.forEach(({ hashtag, avg_sentiment, post_count }) => {
    // EN: Map city/region from hashtag if possible (demo: use hashtag as city name)
  // Forecasting & Global Trends Dashboard Logic
  // EN: All data is fetched securely from backend APIs using API Key authentication. Multilingual support is provided in all UI labels and comments.
  // ES: Todos los datos se obtienen de forma segura desde APIs backend usando autenticación por API Key. Soporte multilingüe en todas las etiquetas y comentarios.
  // EO: Ĉiuj datumoj estas sekure ricevitaj el backend-API-oj per API-ŝlosila aŭtentikigo. Multlingva subteno en ĉiuj etikedoj kaj komentoj.
    // For demo, randomize lat/lng for each hashtag
    const city = hashtag.replace('#','');
  // EN: API Key is required for all requests. ES: Se requiere API Key para todas las peticiones. EO: API-ŝlosilo estas bezonata por ĉiuj petoj.
  const API_KEY = localStorage.getItem('dmgt_api_key') || prompt('Enter API Key for dashboard:');
    // EN: Use avg_sentiment as viral velocity score (0-1)
    const score = Math.max(0, Math.min(1, avg_sentiment));
    const color = score > 0.8 ? '#ff5252' : score > 0.5 ? '#ffeb3b' : '#90caf9';
    const glow = score > 0.8 ? '0 0 32px 12px #ff5252' : score > 0.5 ? '0 0 24px 8px #ffeb3b' : '0 0 16px 6px #90caf9';
    const marker = L.circleMarker([lat, lng], {
  function fetchAuth(url) {
    return fetch(url, { headers: { 'X-API-Key': API_KEY } }).then(r => r.json());
  }
      radius: 18,
      color: color,
      fillColor: color,
      fillOpacity: 0.7,
  // --- Predictive Map (Leaflet + Glow) ---
  // EN: Predictive map shows viral velocity per city/region. Data is fetched securely and visualized with multilingual tooltips.
  // ES: El mapa predictivo muestra velocidad viral por ciudad/región. Datos seguros y tooltips multilingües.
  // EO: Prognoza mapo montras viran rapidecon laŭ urbo/regiono. Sekuraj datumoj kaj multlingvaj konsiletoj.
    }).addTo(map);
    marker._path.style.filter = `drop-shadow(${glow})`;
    marker.bindTooltip(`${city}<br>Viral Velocity: <b>${Math.round(score*100)}%</b><br>Posts: ${post_count}`);
  });
});

// --- Trend Comparison Chart (Chart.js) ---
// EN: Fetch sentiment and arrivals from backend. ES: Consulta sentimiento y llegadas del backend. EO: Ricevu sentimon kaj alvenojn de la backend.
const ctx = document.getElementById('trend-comparison-chart').getContext('2d');
fetchAuth(`${API_BASE}/trends/xiaohongshu`).then(trends => {
  // EN: Use timestamp as label, avg_sentiment as sentiment, post_count as arrivals
  // ES: Usa timestamp como etiqueta, avg_sentiment como sentimiento, post_count como llegadas
  // EO: Uzu timestamp kiel etikedo, avg_sentiment kiel sentimo, post_count kiel alvenoj
  const labels = trends.map(t => (new Date(t.timestamp)).toLocaleDateString());
  const sentiment = trends.map(t => t.avg_sentiment);
  const arrivals = trends.map(t => t.post_count);
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Sentiment / Sentimiento / Sentimo',
          data: sentiment,
          borderColor: '#1a237e',
          backgroundColor: 'rgba(26,35,126,0.08)',
          yAxisID: 'y1',
          tension: 0.3,
  // --- Trend Comparison Chart (Chart.js) ---
  // EN: Trend chart compares sentiment and arrivals over time. Data is securely fetched and labels are multilingual.
  // ES: El gráfico de tendencias compara sentimiento y llegadas en el tiempo. Datos seguros y etiquetas multilingües.
  // EO: Tendenca diagramo komparas sentimon kaj alvenojn laŭ tempo. Sekuraj datumoj kaj multlingvaj etikedoj.
        },
        {
          label: 'Predicted Arrivals / Llegadas / Alvenoj',
          data: arrivals,
          borderColor: '#ff5252',
          backgroundColor: 'rgba(255,82,82,0.08)',
          yAxisID: 'y2',
          tension: 0.3,
          pointRadius: 2
        },
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      stacked: false,
      plugins: {
        legend: { position: 'top' },
        title: { display: false }
      },
      scales: {
        y1: {
          type: 'linear',
          display: true,
          position: 'left',
          min: 0,
          max: 1,
          title: { display: true, text: 'Sentiment' }
        },
        y2: {
          type: 'linear',
          display: true,
          position: 'right',
          min: 0,
          max: 400,
          grid: { drawOnChartArea: false },
          title: { display: true, text: 'Arrivals' }
        }
      }
    }
  });
});

// --- CEO Metrics: Global Footprint (Top Countries) ---
// EN: Fetch top countries by revenue from backend. ES: Consulta los principales países por ingresos del backend. EO: Ricevu la ĉefajn landojn laŭ enspezo de la backend.
fetchAuth(`${API_BASE}/business/revenue`).then(revenueData => {
  // Aggregate by region/country
  const countryMap = {};
  revenueData.forEach(r => {
    countryMap[r.region] = (countryMap[r.region] || 0) + r.amount;
  });
  // Sort by revenue descending
  const sorted = Object.entries(countryMap)
    .map(([country, revenue]) => ({ country, revenue }))
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 5);
  const footprintDiv = document.getElementById('global-footprint');
  footprintDiv.innerHTML = sorted.map(
    (c, i) => `<div><b>${i+1}. ${c.country}</b>: $${c.revenue.toLocaleString()}</div>`
  ).join('');
});

// --- Mobile Critical Alert ---
function showMobileAlert() {
  const alert = document.getElementById('mobile-alert');
  alert.classList.remove('hidden');
  setTimeout(() => alert.classList.add('hidden'), 6000);
  // --- CEO Metrics: Global Footprint (Top Countries) ---
  // EN: Global footprint shows top countries by revenue. Data is securely fetched and displayed with multilingual support.
  // ES: Huella global muestra los principales países por ingresos. Datos seguros y soporte multilingüe.
  // EO: Tutmonda spuro montras la ĉefajn landojn laŭ enspezo. Sekuraj datumoj kaj multlingva subteno.
// Simulate alert if surge >30%
if (arrivals.some((v, i, arr) => i>0 && (v-arr[i-1])/arr[i-1]>0.3)) {
  showMobileAlert();
}
