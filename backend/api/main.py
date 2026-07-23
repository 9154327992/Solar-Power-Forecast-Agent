"""
backend/api/main.py

Solar Power Forecast Agent
FastAPI Backend Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ==========================
# Import Routers
# ==========================

from backend.api.routes.auth import router as auth_router
from backend.api.routes.weather import router as weather_router
from backend.api.routes.prediction import router as prediction_router
from backend.api.routes.history import router as history_router
from backend.api.routes.recommendation import router as recommendation_router
from backend.api.routes.maintenance import router as maintenance_router
from backend.api.routes.battery import router as battery_router

# ==========================
# Database
# ==========================

try:
    from backend.database.database import initialize_database
except Exception:
    initialize_database = None

# ==========================
# FastAPI App
# ==========================

app = FastAPI(
    title="Solar Power Forecast API",
    description="REST API for Solar Power Forecast Agent",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ==========================
# CORS
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Startup Event
# ==========================

@app.on_event("startup")
def startup():

    print("=" * 60)
    print("Solar Power Forecast API Starting...")
    print("=" * 60)

    if initialize_database:
        try:
            initialize_database()
            print("Database initialized")
        except Exception as e:
            print(f"Database initialization failed: {e}")

# ==========================
# Root Endpoint
# ==========================

@app.get("/", tags=["Home"])
def root():

    return {
        "application": "Solar Power Forecast Agent",
        "backend": "FastAPI",
        "version": "1.0.0",
        "status": "Running",
        "documentation": "/docs"
    }

# ==========================
# Health Check
# ==========================

@app.get("/health", tags=["Health"])
def health():

    return {
        "status": "healthy",
        "server": "online"
    }

# ==========================
# API Information
# ==========================

@app.get("/api", tags=["API"])
def api():

    return {
        "Authentication": "/api/auth",
        "Prediction": "/api/predict",
        "Weather": "/api/weather",
        "History": "/api/history",
        "Recommendation": "/api/recommendation",
        "Maintenance": "/api/maintenance",
        "Battery": "/api/battery"
    }

# ==========================
# Register Routers
# ==========================

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"],
)

app.include_router(
    weather_router,
    prefix="/api/weather",
    tags=["Weather"],
)

app.include_router(
    prediction_router,
    prefix="/api/predict",
    tags=["Prediction"],
)

app.include_router(
    history_router,
    prefix="/api/history",
    tags=["History"],
)

app.include_router(
    recommendation_router,
    prefix="/api/recommendation",
    tags=["Recommendation"],
)

app.include_router(
    maintenance_router,
    prefix="/api/maintenance",
    tags=["Maintenance"],
)

app.include_router(
    battery_router,
    prefix="/api/battery",
    tags=["Battery"],
)

# ==========================
# Shutdown Event
# ==========================

@app.on_event("shutdown")
def shutdown():

    print("Solar Power Forecast API Stopped")

# ==========================
# Run Server
# ==========================

if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )