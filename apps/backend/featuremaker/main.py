from fastapi import FastAPI
from featuremaker.routers import health
app = FastAPI()

app.include_router(health.router)
