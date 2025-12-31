from fastapi import FastAPI
from backend.api import onboarding

app = FastAPI()

app.include_router(onboarding.router)
