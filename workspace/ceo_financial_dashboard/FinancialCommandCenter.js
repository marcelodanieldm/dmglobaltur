// FinancialCommandCenter.js
// Fetch and render MRR Growth Over Time
async function renderMRRChart() {
  const resp = await fetch('/api/v1/financial/mrr');
  const data = await resp.json();
  const mrrCtx = document.getElementById('mrrChart').getContext('2d');
  new Chart(mrrCtx, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'MRR',
        data: data.data,
        borderColor: '#bfa14a',
        backgroundColor: 'rgba(191,161,74,0.08)',
        tension: 0.3,
        fill: true
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' }, title: { display: false } }
    }
  });
}

// Fetch and render Consumption Cost vs. Revenue
async function renderCostRevenueChart() {
  const resp = await fetch('/api/v1/financial/cost_revenue');
  const data = await resp.json();
  const costRevenueCtx = document.getElementById('costRevenueChart').getContext('2d');
  new Chart(costRevenueCtx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [
        {
          label: 'Gemini Cost',
          data: data.gemini_cost,
          backgroundColor: '#e57373'
        },
        {
          label: 'User Revenue',
          data: data.user_revenue,
          backgroundColor: '#bfa14a'
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' }, title: { display: false } }
    }
  });
}

// Fetch and render metrics
async function renderMetrics() {
  const resp = await fetch('/api/v1/financial/metrics');
  const data = await resp.json();
  document.getElementById('net-burn-rate').innerText = `$${data.net_burn_rate}`;
  document.getElementById('cac').innerText = `$${data.cac}`;
  document.getElementById('ltv').innerText = `$${data.ltv}`;
  // Fetch recovered revenue
  try {
    const recResp = await fetch('/api/v1/financial/recovered_revenue');
    const recData = await recResp.json();
    document.getElementById('recovered-revenue').innerText = `$${recData.recovered_revenue}`;
  } catch (e) {
    document.getElementById('recovered-revenue').innerText = 'N/A';
  }
}

// Manual Override Button
const overrideBtn = document.getElementById('manual-override');
overrideBtn.onclick = async function() {
  // Simulate granting premium access
  const userId = prompt('Enter user ID to grant premium access:');
  if (userId) {
    const resp = await fetch('/api/v1/financial/manual_override', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId })
    });
    const data = await resp.json();
    document.getElementById('override-status').innerText = data.status;
  }
};

// Initialize dashboard
window.addEventListener('DOMContentLoaded', () => {
  renderMRRChart();
  renderCostRevenueChart();
  renderMetrics();
});
