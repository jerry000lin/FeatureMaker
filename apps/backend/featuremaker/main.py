from fastapi import FastAPI
from featuremaker.routers import health
from featuremaker.routers import tables
app = FastAPI()

app.include_router(health.router)
app.include_router(tables.router)