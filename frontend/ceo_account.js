// CEO Account Dashboard Logic
// EN / ES / EO

const API_BASE = 'http://localhost:8000/api/v1/business'; // Cambia si usas otro host
const API_KEY = localStorage.getItem('dmgt_api_key') || prompt('Enter API Key for CEO dashboard:');

function fetchAuth(url) {
  return fetch(url, { headers: { 'X-API-Key': API_KEY } }).then(r => r.json());
}

// --- Balance Sheet View (Chart.js) ---
async function renderBalanceSheet() {
  // EN: Fetch revenue and cost by month. ES: Consulta ingresos y costos por mes. EO: Ricevu enspezojn kaj kostojn monate.
  const [revenue, cost] = await Promise.all([
    fetchAuth(`${API_BASE}/revenue`),
    fetchAuth(`${API_BASE}/cost`)
  ]);
  // Group by month
  function groupByMonth(arr, key) {
    const out = {};
    arr.forEach(x => {
      const m = (new Date(x.timestamp)).toLocaleString('default', { month: 'short', year: '2-digit' });
      out[m] = (out[m] || 0) + x[key];
    });
    return out;
  }
  const revByMonth = groupByMonth(revenue, 'amount');
  const costByMonth = groupByMonth(cost, 'amount');
  const months = Array.from(new Set([...Object.keys(revByMonth), ...Object.keys(costByMonth)])).sort();
  const grossRevenue = months.map(m => revByMonth[m] || 0);
  const operatingCosts = months.map(m => costByMonth[m] || 0);
  const ctx = document.getElementById('balance-sheet-chart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: months,
      datasets: [
        {
          label: 'Gross Revenue / Ingresos Brutos / Bruta Enspezo',
          data: grossRevenue,
          backgroundColor: '#43a047',
        },
        {
          label: 'Operating Costs / Costos Operativos / Operaciaj Kostoj',
          data: operatingCosts,
          backgroundColor: '#ff7043',
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: false }
      }
    }
  });
}

// --- Dynamic Break-even Analysis ---
async function renderBreakEven() {
  // EN: Fetch users by region. ES: Consulta usuarios por región. EO: Ricevu uzantojn laŭ regiono.
  const users = await fetchAuth(`${API_BASE}/user`);
  const revenue = await fetchAuth(`${API_BASE}/revenue`);
  const cost = await fetchAuth(`${API_BASE}/cost`);
  // Calculate per region
  const regions = [...new Set(users.map(u => u.region))];
  const table = document.getElementById('break-even-table');
  let html = `<table><tr><th>Region</th><th>Current Users</th><th>Needed for Break-even</th></tr>`;
  regions.forEach(region => {
    const userCount = users.filter(u => u.region === region).length;
    const rev = revenue.filter(r => r.region === region).reduce((a, b) => a + b.amount, 0);
    const cst = cost.filter(c => c.region === region).reduce((a, b) => a + b.amount, 0);
    const needed = rev > 0 ? Math.ceil(userCount * (cst / (rev || 1))) : 'N/A';
    html += `<tr><td>${region}</td><td>${userCount}</td><td>${needed}</td></tr>`;
  });
  html += '</table>';
  table.innerHTML = html;
}

// --- VIP Support (Tier 3) ---
async function renderVIP() {
  // EN: Fetch Tier 3 clients. ES: Consulta clientes Tier 3. EO: Ricevu Tier 3-klientojn.
  const clients = await fetchAuth(`${API_BASE}/client?tier=enterprise`);
  const table = document.getElementById('vip-support-table');
  let html = `<table><tr><th>Client</th><th>Usage (API Calls)</th><th>Last Active</th></tr>`;
  clients.forEach(c => {
    html += `<tr><td>${c.name}</td><td>${c.usage}</td><td>${c.last_active.split('T')[0]}</td></tr>`;
  });
  html += '</table>';
  table.innerHTML = html;
}

// --- Scaling Metrics: Cost per API Call ---
async function renderCostPerApi() {
  // EN: Calculate cost per API call. ES: Calcula costo por llamada API. EO: Kalkulu koston por API-voko.
  const cost = await fetchAuth(`${API_BASE}/cost`);
  const clients = await fetchAuth(`${API_BASE}/client`);
  const totalApiCalls = clients.reduce((a, b) => a + b.usage, 0);
  const totalCosts = cost.reduce((a, b) => a + b.amount, 0);
  const costPerApi = totalApiCalls > 0 ? (totalCosts / totalApiCalls).toFixed(4) : 'N/A';
  document.getElementById('cost-per-api').innerHTML =
    `<b>Cost per API Call / Costo por Llamada API / Kosto por API-voko:</b> $${costPerApi}`;
}

// --- Main render ---
window.addEventListener('DOMContentLoaded', () => {
  renderBalanceSheet();
  renderBreakEven();
  renderVIP();
  renderCostPerApi();
});
