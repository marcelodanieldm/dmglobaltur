// CEO Dashboard Logic for DM Global Tur
// ENGLISH / ESPAÑOL / ESPERANTO

// EN: Simulated data fetch (replace with Supabase/API calls in production)
// ES: Simulación de datos (reemplazar por Supabase/API en producción)
// EO: Simulita datuma akiro (anstataŭigi per Supabase/API en produktado)

document.addEventListener('DOMContentLoaded', () => {
  // Revenue
  document.getElementById('revenue').textContent = '¥ 120,000 / $16,800';
  // New Users per Region
  document.getElementById('users-region').textContent = 'China: 120 | Brazil: 30 | USA: 25';
  // Churn Rate
  document.getElementById('churn').textContent = '3.2%';

  // Break-even Calculator (Chart.js)
  const ctx = document.getElementById('breakevenChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [
        {
          label: 'Server + API Cost',
          data: [2000, 2200, 2500, 2700, 3000, 3200],
          borderColor: '#E63946',
          backgroundColor: 'rgba(230,57,70,0.1)',
          tension: 0.3
        },
        {
          label: 'Subscription Revenue',
          data: [1800, 2100, 2600, 3100, 3500, 4000],
          borderColor: '#FFD700',
          backgroundColor: 'rgba(255,215,0,0.1)',
          tension: 0.3
        }
      ]
    },
    options: {
      plugins: {
        legend: { labels: { color: '#181818' } }
      },
      scales: {
        x: { ticks: { color: '#181818' } },
        y: { ticks: { color: '#181818' } }
      }
    }
  });

  // API Logs Table
  const logs = [
    { customer: 'DMC China', endpoint: '/api/v1/recommend/vibe-matching', calls: 120 },
    { customer: 'Luxury Hotel BR', endpoint: '/api/v1/recommend/scarcity', calls: 80 },
    { customer: 'Travel App US', endpoint: '/api/v1/trends/xiaohongshu', calls: 60 }
  ];
  const tbody = document.querySelector('#api-logs-table tbody');
  logs.forEach(log => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${log.customer}</td><td>${log.endpoint}</td><td>${log.calls}</td>`;
    tbody.appendChild(tr);
  });

  // Heatmap (simulate with colored divs)
  const heatmap = document.getElementById('heatmap');
  heatmap.innerHTML = `
    <div style='width:30%;height:100%;float:left;background:#FFD700;opacity:0.7;text-align:center;color:#181818;padding-top:120px;'>USA<br>High</div>
    <div style='width:30%;height:100%;float:left;background:#E63946;opacity:0.7;text-align:center;color:#fff;padding-top:120px;'>Europe<br>Medium</div>
    <div style='width:40%;height:100%;float:left;background:#181818;opacity:0.7;text-align:center;color:#FFD700;padding-top:120px;'>SE Asia<br>Low</div>
  `;
});
