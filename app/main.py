from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Face Recognition Service")

app.include_router(router)
