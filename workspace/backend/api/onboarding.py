from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
import tempfile
import shutil
from data_science.onboarding_gemini_insight import analyze_inventory_and_generate_insight

router = APIRouter()

@router.post('/api/onboarding/analyze')
def onboarding_analyze(
    city: str = Form(...),
    archetypes: str = Form(...),
    channels: str = Form(...),
    user_id: str = Form(...),
    inventory: UploadFile = None
):
    # Guardar archivo temporalmente
    if inventory:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            shutil.copyfileobj(inventory.file, tmp)
            inventory_path = tmp.name
    else:
        return JSONResponse({'error': 'No inventory file'}, status_code=400)
    # Llamar análisis Gemini
    result = analyze_inventory_and_generate_insight(
        inventory_csv_path=inventory_path,
        city=city,
        archetypes=archetypes,
        user_id=user_id
    )
    return result
