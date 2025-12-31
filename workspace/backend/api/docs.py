from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import FastAPI

app = FastAPI()

@app.get('/api-docs', include_in_schema=False)
def swagger_ui():
    return get_swagger_ui_html(openapi_url='/openapi.json', title='API Docs')

@app.get('/redoc', include_in_schema=False)
def redoc_ui():
    return get_redoc_html(openapi_url='/openapi.json', title='API Docs')
