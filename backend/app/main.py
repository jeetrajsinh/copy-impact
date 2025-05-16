# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analysis
from app.core.config import settings

app = FastAPI(title="Meme Coin Copy Trader API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS, # Origins allowed to make requests
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

app.include_router(analysis.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Meme Coin Copy Trader API"}

# To run: uvicorn app.main:app --reload (from backend directory)