from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import APP_NAME, FRONTEND_ORIGIN
from backend.routes import router

app = FastAPI(
    title=APP_NAME,
    description="AI-powered legal document drafting API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "LegalEase API is running",
        "docs": "/docs",
        "health": "/health",
    }
