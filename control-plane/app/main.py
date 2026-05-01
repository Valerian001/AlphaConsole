from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.compute import router as compute_router
from app.api.objectives import router as objectives_router
from app.api.reviewer import router as reviewer_router

app = FastAPI(
    title="AlphaConsole Control Plane",
    description="Permanent brain and orchestration engine for AlphaConsole.",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(compute_router)
app.include_router(objectives_router)
app.include_router(reviewer_router)

@app.get("/")
async def root():
    return {
        "status": "active",
        "service": "AlphaConsole Control Plane",
        "version": settings.VERSION
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
