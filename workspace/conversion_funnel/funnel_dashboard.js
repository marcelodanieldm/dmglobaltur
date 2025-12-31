// funnel_dashboard.js
// Fetch real-time data from FastAPI backend
async function fetchReports() {
  const resp = await fetch("/api/v1/funnel/reports");
  const data = await resp.json();
  return data.reports || [];
}

async function renderTable() {
  const reports = await fetchReports();
  const tbody = document.querySelector("#report-table tbody");
  tbody.innerHTML = "";
  reports.forEach(r => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${r.user_id}</td>
      <td>${r.time_to_value}</td>
      <td class="${r.high_intent ? 'high-intent' : 'low-intent'}">${r.high_intent ? 'High' : 'Low'}</td>
      <td>${r.recommendation}</td>
    `;
    tbody.appendChild(tr);
  });
}

document.addEventListener("DOMContentLoaded", renderTable);
