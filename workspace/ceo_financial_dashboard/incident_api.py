"""
Incident Management API for QA Dashboard
- List, update, and audit incidents detected by Watchdog
"""
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import datetime
import uuid

app = FastAPI()

# In-memory store (replace with DB in prod)
INCIDENTS = []
AUDIT_LOG = []

class Incident(BaseModel):
    id: str
    titulo: str
    estado: str  # Abierto, Investigando, Resuelto
    diagnosis: str
    log: List[dict]

class IncidentAction(BaseModel):
    usuario: str
    accion: str
    fecha: str

@app.get("/api/incidents", response_model=List[Incident])
def list_incidents():
    return INCIDENTS

@app.post("/api/incidents/{incident_id}/action")
def incident_action(incident_id: str, action: IncidentAction):
    for inc in INCIDENTS:
        if inc['id'] == incident_id:
            inc['estado'] = action.accion if action.accion in ['Abierto','Investigando','Resuelto'] else inc['estado']
            inc['log'].append({'usuario': action.usuario, 'accion': action.accion, 'fecha': action.fecha})
            AUDIT_LOG.append({'usuario': action.usuario, 'accion': action.accion, 'fecha': action.fecha, 'incidente': inc['titulo']})
            return {"status": "ok"}
    raise HTTPException(404, "Incidente no encontrado")

@app.get("/api/audit_log")
def get_audit_log():
    return AUDIT_LOG

@app.post("/api/incidents/{incident_id}/pause_api")
def pause_api(incident_id: str, request: Request):
    # Aquí iría la lógica real para pausar Gemini para el cliente afectado
    return {"status": "API Gemini pausada para incidente " + incident_id}

@app.post("/api/incidents/{incident_id}/retry_webhook")
def retry_webhook(incident_id: str, request: Request):
    # Aquí iría la lógica real para reintentar el webhook de Stripe
    return {"status": "Webhook reintentado para incidente " + incident_id}

# Demo: poblar con incidentes simulados al iniciar
@app.on_event("startup")
def seed():
    if not INCIDENTS:
        INCIDENTS.extend([
            {
                'id': str(uuid.uuid4()),
                'titulo': 'Caída de Ventas',
                'estado': 'Abierto',
                'diagnosis': 'Probable: Error de conexión con Stripe en región EU.',
                'log': []
            },
            {
                'id': str(uuid.uuid4()),
                'titulo': 'Fallo de Pasarela Alipay',
                'estado': 'Investigando',
                'diagnosis': 'Probable: Webhook rechazado por timeout en Asia-Pacífico.',
                'log': [
                    {'usuario': 'Daniel', 'accion': 'Cambiado a Investigando', 'fecha': '2025-12-30 09:12'}
                ]
            },
            {
                'id': str(uuid.uuid4()),
                'titulo': 'Consumo Anómalo de Gemini',
                'estado': 'Resuelto',
                'diagnosis': 'Probable: Bucle en endpoint /forecasting, mitigado.',
                'log': [
                    {'usuario': 'Daniel', 'accion': 'Resuelto: Limitar llamadas por IP', 'fecha': '2025-12-30 08:45'}
                ]
            }
        ])
