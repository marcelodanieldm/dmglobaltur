from fastapi import APIRouter, Depends
from backend.api.api_key_manager import assign_api_key_to_user, get_api_key
from backend.api.auth import get_current_user

router = APIRouter()

@router.post('/api/v1/tier3/activate_api_key')
def activate_api_key(user=Depends(get_current_user)):
    if user['tier'] < 3:
        return {"error": "Forbidden"}
    api_key = get_api_key(user['id'])
    if not api_key:
        api_key = assign_api_key_to_user(user['id'])
    return {"api_key": api_key}
