from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import API routers
from backend.api.routes import (
    auth,
    weather,
    prediction,
    history,
    recommendation,
    maintenance,
    battery,
)

app = FastAPI(
    title="Solar Power Forecast Agent API",
    description="AI-powered Solar Power Forecasting REST API",
    version="1.0.0",
)

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Root Endpoint
# -------------------------
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Solar Power Forecast Agent running successfully",
        "version": "1.0.0"
    }


# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Solar Power Forecast Agent API"
    }


# -------------------------
# API Information
# -------------------------
@app.get("/api")
def api_info():
    return {
        "name": "Solar Power Forecast Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# -------------------------
# Register Routers
# -------------------------
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(
    weather.router,
    prefix="/api/weather",
    tags=["Weather"]
)

app.include_router(
    prediction.router,
    prefix="/api/predict",
    tags=["Prediction"]
)

app.include_router(
    history.router,
    prefix="/api/history",
    tags=["History"]
)

app.include_router(
    recommendation.router,
    prefix="/api/recommendation",
    tags=["Recommendation"]
)

app.include_router(
    maintenance.router,
    prefix="/api/maintenance",
    tags=["Maintenance"]
)

app.include_router(
    battery.router,
    prefix="/api/battery",
    tags=["Battery"]
)


# -------------------------
# Startup Event
# -------------------------
@app.on_event("startup")
def startup():
    print("Solar Power Forecast Agent API started successfully.")


# -------------------------
# Shutdown Event
# -------------------------
@app.on_event("shutdown")
def shutdown():
    print("Solar Power Forecast Agent API stopped.")


# -------------------------
# Run with Uvicorn
# -------------------------
if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
