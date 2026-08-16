from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.services.ai_service import ai_service
from backend.services.blockchain_service import blockchain_service
from backend.routes import analysis, blockchain

# Initialize FastAPI App
app = FastAPI(
    title="TrustChain API",
    description="AI Document Forgery Detection & Blockchain Verification Platform",
    version="2.0.0"
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if "*" not in settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Endpoint for ELA Output Images
app.mount("/ela_outputs", StaticFiles(directory=settings.ELA_DIR), name="ela_outputs")

# Register Routers
app.include_router(analysis.router)
app.include_router(blockchain.router)

# Root System Health Endpoints
@app.get("/")
def home():
    return {
        "status": "online",
        "system": "TrustChain AI Forgery Detection & Blockchain Platform",
        "version": "2.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "blockchain_connected": blockchain_service.is_connected(),
        "model_loaded": ai_service.model is not None
    }