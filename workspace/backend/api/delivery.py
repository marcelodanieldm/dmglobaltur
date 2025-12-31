from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from backend.notifications.whatsapp import send_whatsapp_alert
from backend.api.auth import get_current_user
from backend.api.cache import get_cached_insights, set_cached_insights
import time

router = APIRouter()

@router.get('/api/v1/delivery/insights')
def get_insights(user=Depends(get_current_user)):
    # Cache 6h salvo alertas críticas
    cache_key = f"insights_{user['id']}"
    cached, ts = get_cached_insights(cache_key)
    if cached and time.time() - ts < 6*60*60:
        return cached
    # ...fetch real insights...
    # set_cached_insights(cache_key, data)
    return {"insights": []}

@router.post('/api/v1/delivery/alert')
def send_alert(payload: dict, user=Depends(get_current_user)):
    # Solo para insights críticos
    if payload.get('type') == 'critical':
        phone = user.get('whatsapp')
        if phone:
            ok = send_whatsapp_alert(phone, payload.get('message', ''))
            return JSONResponse({'sent': ok})
    return JSONResponse({'sent': False})
