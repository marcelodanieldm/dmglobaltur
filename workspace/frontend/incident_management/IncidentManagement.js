
let INCIDENTS = [];

async function fetchIncidents() {
  const resp = await fetch('/api/incidents');
  INCIDENTS = await resp.json();
}

async function fetchAuditLog() {
  const resp = await fetch('/api/audit_log');
  return await resp.json();
}

async function renderIncidents() {
  await fetchIncidents();
  const list = document.getElementById('incident-list');
  list.innerHTML = '';
  INCIDENTS.forEach(inc => {
    const div = document.createElement('div');
    div.className = 'incident ' + inc.estado.toLowerCase();
    div.innerHTML = `
      <div class="incident-header">
        <span class="incident-title">${inc.titulo}</span>
        <span class="incident-status">${inc.estado}</span>
      </div>
      <div class="incident-actions">
        ${inc.estado !== 'Resuelto' ? `
          <button class="pause" onclick="pauseApi('${inc.id}')">PAUSAR API</button>
          <button class="retry" onclick="retryWebhook('${inc.id}')">REINTENTAR WEBHOOK</button>
          <button onclick="changeStatus('${inc.id}','Investigando')">INVESTIGANDO</button>
          <button onclick="changeStatus('${inc.id}','Resuelto')">RESUELTO</button>
        ` : ''}
      </div>
      <div class="incident-diagnosis">Causa Probable: ${inc.diagnosis}</div>
      <div class="incident-log">
        ${inc.log && inc.log.length ? '<b>Log:</b><ul>' + inc.log.map(l => `<li>${l.fecha} - ${l.usuario}: ${l.accion}</li>`).join('') + '</ul>' : ''}
      </div>
    `;
    list.appendChild(div);
  });
}

async function renderAuditLog() {
  const audit = document.getElementById('audit-entries');
  const log = await fetchAuditLog();
  audit.innerHTML = '';
  log.forEach(l => {
    audit.innerHTML += `<li>${l.fecha} - <b>${l.usuario}</b>: ${l.accion} (${l.incidente})</li>`;
  });
}

async function pauseApi(id) {
  await fetch(`/api/incidents/${id}/pause_api`, {method: 'POST'});
  alert('API Gemini pausada para el cliente afectado (Incidente ' + id + ').');
}
async function retryWebhook(id) {
  await fetch(`/api/incidents/${id}/retry_webhook`, {method: 'POST'});
  alert('Webhook de Stripe reintentado para el incidente ' + id + '.');
}

async function changeStatus(id, status) {
  const usuario = prompt('¿Quién realiza la acción?');
  if (!usuario) return;
  const fecha = new Date().toISOString().replace('T',' ').substring(0,16);
  await fetch(`/api/incidents/${id}/action`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({usuario, accion: status, fecha})
  });
  await renderIncidents();
  await renderAuditLog();
}

window.onload = async function() {
  await renderIncidents();
  await renderAuditLog();
};
