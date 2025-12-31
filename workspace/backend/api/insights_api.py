from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from backend.api.auth import get_current_user

router = APIRouter()
api_key_header = APIKeyHeader(name="x-api-key")

@router.get('/api/v1/insights')
def api_insights(user=Depends(get_current_user), api_key=Depends(api_key_header)):
    # Validar API key y tier
    if user['tier'] < 3 or user['api_key'] != api_key:
        return {"error": "Forbidden"}
    # ...fetch insights...
    return {"insights": []}
